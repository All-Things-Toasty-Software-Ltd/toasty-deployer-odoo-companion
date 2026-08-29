# Part of The Baker's Archive. See LICENSE file for full copyright and licensing details.

{
    'name': "Toasty Deployer",
    'category': 'Toasty Software',
    'sequence': 200,
    'website': 'https://www.toastysoftware.co.uk',
    'summary': "Track Toasty Deployer builds across GitHub repos inside Odoo",
    'version': '0.1.0',
    'depends': ['base'],

    'currency': 'EUR',
    'price': 0.00,
    'description': """
Toasty Deployer
===============

Integrates Toasty Deployer CI/CD status into Odoo.
Features GitHub profile mirroring, repo listing, and build terminal logs.
    """,
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/res_config_settings_views.xml',
        'views/toasty_deployer_owner_views.xml',
        'views/toasty_deployer_repo_views.xml',
        'views/toasty_deployer_run_views.xml',
        'views/toasty_deployer_menu_views.xml',
    ],
    'author': 'All Things Toasty Software Ltd',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
