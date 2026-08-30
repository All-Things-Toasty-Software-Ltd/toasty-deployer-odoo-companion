# -*- coding: utf-8 -*-
# Part of Toasty Deployer. See LICENSE file for additional copyright and licensing details.

import base64
import logging
import requests

from odoo import models, api

_logger = logging.getLogger(__name__)


class ToastyDeployerGithubSync(models.TransientModel):
    _name = 'toasty_deployer.github_sync'
    _description = 'Toasty Deployer GitHub Sync'

    @api.model
    def sync_owner(self, owner):
        """Fetch and store GitHub information for an owner."""

        if not owner.name:
            return False

        try:
            response = requests.get(
                f"https://api.github.com/users/{owner.name}",
                timeout=15,
            )
            response.raise_for_status()

            data = response.json()

            owner.write({
                'github_url': data.get('html_url') or f"https://github.com/{owner.name}",
                'avatar_url': data.get('avatar_url') or '',
                'bio': data.get('bio') or '',
            })

            if data.get('avatar_url'):
                self._sync_avatar(owner, data['avatar_url'])

            return True

        except requests.exceptions.RequestException as e:
            _logger.warning(
                "Toasty Deployer: Failed to sync GitHub owner '%s': %s",
                owner.name,
                e,
            )
            return False

    @api.model
    def sync_repo(self, repo):
        """Fetch and store GitHub information for a repository."""

        if not repo.owner_id or not repo.name:
            return False

        try:
            response = requests.get(
                f"https://api.github.com/repos/"
                f"{repo.owner_id.name}/{repo.name}",
                timeout=15,
            )
            response.raise_for_status()

            data = response.json()

            repo.write({
                'github_url': data.get('html_url') or '',
                'description': data.get('description') or '',
            })

            return True

        except requests.exceptions.RequestException as e:
            _logger.warning(
                "Toasty Deployer: Failed to sync GitHub repo '%s/%s': %s",
                repo.owner_id.name,
                repo.name,
                e,
            )
            return False

    @api.model
    def _sync_avatar(self, owner, avatar_url):
        """Download and store an owner's GitHub avatar."""

        try:
            response = requests.get(
                avatar_url,
                timeout=15,
            )
            response.raise_for_status()

            owner.write({
                'avatar_image': base64.b64encode(response.content),
            })

        except requests.exceptions.RequestException as e:
            _logger.warning(
                "Toasty Deployer: Failed to download avatar for '%s': %s",
                owner.name,
                e,
            )


    @api.model
    def sync_all(self):
        Owner = self.env['toasty_deployer.owner'].sudo()
        Repo = self.env['toasty_deployer.repo'].sudo()

        owners = Owner.search([])

        owner_count = 0
        repo_count = 0

        for owner in owners:
            if self.sync_owner(owner):
                owner_count += 1

            for repo in owner.repo_ids:
                if self.sync_repo(repo):
                    repo_count += 1

        _logger.info(
            "Toasty Deployer: GitHub sync completed. "
            "Synced %d owners and %d repositories.",
            owner_count,
            repo_count,
        )

        return {
            'owners': owner_count,
            'repositories': repo_count,
        }

    def action_sync_all(self):
        self.sync_all()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'GitHub Sync',
                'message': 'GitHub data has been synchronised successfully.',
                'type': 'success',
                'sticky': False,
            },
        }