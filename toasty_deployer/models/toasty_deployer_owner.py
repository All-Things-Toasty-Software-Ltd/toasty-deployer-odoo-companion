# -*- coding: utf-8 -*-
# Part of Toasty Deployer. See LICENSE file for full copyright and licensing details.

import requests
from odoo import models, fields, api


class ToastyDeployerOwner(models.Model):
    _name = 'toasty_deployer.owner'
    _description = 'Toasty Deployer Owner'

    name = fields.Char(string='Owner Name', required=True, index=True)
    github_url = fields.Char(string='GitHub Page', compute='_compute_github_url')
    avatar_url = fields.Char(string='Avatar Page', compute='_compute_avatar_url')
    bio = fields.Char(string='Bio / Description', compute='_compute_bio')
    repo_ids = fields.One2many('toasty_deployer.repo', 'owner_id', string="Repositories")

    @api.depends('name')
    def _compute_github_url(self):
        for rec in self:
            rec.github_url = f"https://github.com/{rec.name}" if rec.name else "#"

    @api.depends('name')
    def _compute_avatar_url(self):
        for rec in self:
            if not rec.name:
                continue
            res = requests.get(f"https://api.github.com/users/{rec.name}", timeout=10)
            if res.status_code == 200:
                data = res.json()
                rec.write({
                    'avatar_url': data.get('avatar_url'),
                })

    @api.depends('name')
    def _compute_bio(self):
        for rec in self:
            if not rec.name:
                continue
            res = requests.get(f"https://api.github.com/users/{rec.name}", timeout=10)
            if res.status_code == 200:
                data = res.json()
                rec.write({
                    'bio': data.get('bio'),
                })
