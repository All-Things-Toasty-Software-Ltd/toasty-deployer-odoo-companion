# -*- coding: utf-8 -*-
# Part of Toasty Deployer. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ToastyDeployerRepo(models.Model):
    _name = 'toasty_deployer.repo'
    _description = 'Toasty Deployer Repo'

    name = fields.Char(string='Repository Name', required=True)
    owner_id = fields.Many2one('toasty_deployer.owner', string='Owner', ondelete='cascade', required=True)
    description = fields.Char(string='Description')
    github_url = fields.Char(string='GitHub URL')
    run_ids = fields.One2many('toasty_deployer.run', 'repo_id', string='Build Runs')
    latest_run_id = fields.Many2one('toasty_deployer.run', string='Latest Run', compute='_compute_latest_run_id',
                                    store=True)
    latest_status = fields.Selection(related='latest_run_id.status', string='Latest Status')

    @api.depends('run_ids', 'run_ids.status', 'run_ids.created_at')
    def _compute_latest_run_id(self):
        for rec in self:
            rec.latest_run_id = rec.run_ids[:1] or False
