# -*- coding: utf-8 -*-
# Part of Toasty Deployer. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ToastyDeployerOwner(models.Model):
    _name = 'toasty_deployer.owner'
    _description = 'Toasty Deployer Owner'

    name = fields.Char(string='Owner Name', required=True, index=True)
    github_url = fields.Char(string='GitHub Page')
    avatar_url = fields.Char(string='Avatar Page')
    avatar_image = fields.Binary(string='Avatar Image', attachment=True)
    bio = fields.Char(string='Bio / Description')
    repo_ids = fields.One2many('toasty_deployer.repo', 'owner_id', string="Repositories")
