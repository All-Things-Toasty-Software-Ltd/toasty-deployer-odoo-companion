# -*- coding: utf-8 -*-
# Part of Toasty Deployer. See LICENSE file for full copyright and licensing details.

import requests
from odoo import models, fields, api


class ToastyDeployerRepo(models.Model):
    _name = 'toasty.deployer.repo'
    _description = 'Toasty Deployer Repo'

    name = fields.Char(string='Repository Name', required=True)
    owner_id = fields.Many2one('toasty.deployer.owner', string='Owner', ondelete='cascade')
    description = fields.Char(string='Description', compute='_compute_description')
    github_url = fields.Char(string='GitHub URL', compute='_compute_github_url')
    run_ids = fields.One2many('toasty.deployer.run', 'repo_id', string='Build Runs')
    latest_run_id = fields.Many2one('toasty.deployer.run', string='Latest Run', compute='_compute_latest_run_id')
    latest_status = fields.Selection(related='latest_run_id.status', string='Latest Status')

    @api.depends('name', 'owner_id.name')
    def _compute_description(self):
        for rec in self:
            if not rec.owner_id and rec.name:
                continue
            res = requests.get(f"https://api.github.com/repos/{rec.owner_id.name}/{rec.name}", timeout=10)
            if res.status_code == 200:
                data = res.json()
                rec.write({
                    'description': data.get('description'),
                })


    @api.depends('name', 'owner_id.name')
    def _compute_github_url(self):
        for rec in self:
            rec.github_url = f"https://github.com/{rec.owner_id.name}/{rec.name}" if rec.owner_id and rec.name else "#"

    @api.depends('run_ids', 'run_ids.status', 'run_ids.created_at')
    def _compute_latest_run_id(self):
        for rec in self:
            rec.latest_run_id = rec.run_ids.sorted(key=lambda r: r.created_at or '', reverse=True)[:1]