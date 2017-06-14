# -*- coding: utf-8 -*-
# Copyright 2016-2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Purchase Document Print",
    "summary": "",
    "version": "10.0.1.1.1",
    "category": "Purchases",
    "website": "https://www.odoo-asia.com/",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "pre_init_hook": "",
    "post_init_hook": "",
    "post_load": "",
    "uninstall_hook": "",
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "purchase",
        "report_common_nrq",
    ],
    "data": [
        'report/purchase_report_template.xml'
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
