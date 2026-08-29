# -*- coding: utf-8 -*-
# Part of Toasty Deployer. See LICENSE file for full copyright and licensing details.

import requests
from odoo import models, fields, api


class ToastyDeployerRun(models.Model):
    _name = 'toasty.deployer.run'
    _description = 'Toasty Deployer Run'
    _order = 'created_at desc, id desc'

    name = fields.Char(string='Run ID / Name', required=True)
    repo_id = fields.Many2one('toasty.deployer.repo', string='Repository', ondelete='cascade', required=True)
    commit_sha = fields.Char(string='Commit SHA')
    status = fields.Selection([
        ('running', 'Running'),
        ('success', 'Success'),
        ('failure', 'Failure'),
    ], string='Status', default='running', required=True)
    exit_code = fields.Integer(string='Exit Code')
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now)
    logs = fields.Text(string='Logs')