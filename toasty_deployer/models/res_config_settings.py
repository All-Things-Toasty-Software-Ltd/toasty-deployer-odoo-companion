# -*- coding: utf-8 -*-
# Part of Toasty Deployer. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    toasty_deployer_base_url = fields.Char(string="Toasty Deployer Server URL",
                                           help="The Base URL where your Toasty Deployer instance is hosted.",
                                           readonly=False, required=True, config_parameter='toasty_deployer.base_url',
                                           default="https://deploy.toastysoftware.co.uk")
