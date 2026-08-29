# -*- coding: utf-8 -*-
# Part of Toasty Deployer. See LICENSE file for full copyright and licensing details.

import logging
import requests
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class ToastyDeployerRun(models.TransientModel):
    _name = 'toasty_deployer.sync_service'
    _description = 'Toasty Deployer Sync Service'

    @api.model
    def _get_base_url(self):
        """Retrieves the Toasty Deployer Base URL"""
        IrConfigParameter = self.env['ir.config_parameter'].sudo()
        try:
            raw_url = IrConfigParameter.get_param('toasty_deployer.base_url', default='')
        except AttributeError:
            param = IrConfigParameter.search([('key', '=', 'toasty_deployer.base_url')], limit=1)
            raw_url = param.value if param else ''

        if not raw_url:
            _logger.warning("Toasty Deployer: 'toasty_deployer.base_url' config parameter is missing or empty.")
            return ''

        return raw_url.rstrip('/')

    @api.model
    def _cron_sync_all_deployments(self):
        """Discovers the owners/repos and syncs the deployment runs from the Toasty Deployer API."""
        base_url = self._get_base_url()
        if not base_url:
            _logger.error("Toasty Deployer: Sync aborted. Base URL is not configured.")
            return False

        # Ensure base URL hits /api
        api_base = f"{base_url}/api" if not base_url.endswith("/api") else base_url
        _logger.info("Toasty Deployer: Starting full sync against %s", api_base)

        session = requests.Session()

        # GET /api/owners
        try:
            res_owners = session.get(f"{api_base}/owners", timeout=15)
            res_owners.raise_for_status()
            owners_data = res_owners.json().get('owners', [])
        except requests.exception.RequestException as e:
            _logger.error("Toasty Deployer: Failed to fetch owners list: %s", str(e))
            return False

        Owner = self.env['toasty_deployer.owner'].sudo()
        Repo = self.env['toasty_deployer.repo'].sudo()
        Run = self.env['toasty_deployer.run'].sudo()

        total_synced_runs = 0

        # Iterate owners.
        for owner_name in owners_data:
            owner = Owner.search([('name', '=', owner_name)], limit=1)
            if not owner:
                owner = Owner.create({'name': owner_name})

            # GET /api/owners/<owner>
            try:
                res_repos = session.get(f"{api_base}/owners/{owner_name}", timeout=15)
                res_repos.raise_for_status()
                repos_data = res_repos.json().get('repositories', [])
            except requests.exception.RequestException as e:
                _logger.warning("Toasty Deployer: Failed to fetch repos for owner '%s': '%s'", owner_name, str(e))
                continue

            # Iterate repos
            for repo_name in repos_data:
                repo = Repo.search([
                    ('name', '=', repo_name),
                    ('owner_id', '=', owner.id),
                ], limit=1)

                if not repo:
                    repo = Repo.create({
                        'name': repo_name,
                        'owner_id': owner.id,
                    })

                # GET /api/owners/<owner>/<repo>
                try:
                    res_runs = session.get(f"{api_base}/owners/{owner_name}/{repo_name}", timeout=15)
                    res_runs.raise_for_status()
                    runs_data = res_runs.json().get('runs', [])
                except requests.exception.RequestException as e:
                    _logger.warning("Toasty Deployer: Failed to fetch runs for %s/%s: %s", owner_name, repo_name,
                                    str(e))
                    continue

                # Sync in Odoo
                for run_item in runs_data:
                    run_id_str = str(run_item.get('id'))
                    if not run_id_str:
                        continue

                    commit_sha = run_item.get('commit_sha') or 'HEAD'
                    raw_status = (run_item.get('status') or 'running').lower()
                    status = 'success' if raw_status == 'success' else 'failure' if raw_status == 'failure' else 'running'
                    exit_code = run_item.get('exit_code') or 0
                    created_at = run_item.get('created_at') or fields.Datetime.now()
                    logs = run_item.get('logs') or ''

                    # Find existing run or create new
                    run = Run.search([
                        ('name', '=', run_id_str),
                        ('repo_id', '=', repo.id),
                    ], limit=1)

                    if run:
                        run.write({
                            'status': status,
                            'exit_code': exit_code,
                            'logs': logs,
                        })
                    else:
                        Run.create({
                            'name': run_id_str,
                            'repo_id': repo.id,
                            'commit_sha': commit_sha,
                            'status': status,
                            'exit_code': exit_code,
                            'created_at': created_at,
                            'logs': logs,
                        })

                    total_synced_runs += 1

        _logger.info("Toasty Deployer: Sync finished successfully. Synced %d runs.", total_synced_runs)
        return True
