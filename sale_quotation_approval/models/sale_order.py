# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval = fields.Boolean(
        string='Approved',
        compute='_update_approve',
        store=True,
        readonly=True,
        default=False,
        copy=False,
        track_visibility='onchange',
    )

    @api.multi
    def write(self, vals):
        if 'state' in vals:
            for quote in self:
                if vals['state'] == "cancel":
                    vals['approval'] = False
                elif (quote.state == "draft" and quote.approval) or vals['state'] in ["sale", "done"]:
                    vals['approval'] = True
                elif quote.state != "draft":
                    vals['approval'] = False
        res = super(SaleOrder, self).write(vals)
        return res

    @api.multi
    def action_approve(self):
        for quote in self:
            quote.approval = True

    @api.multi
    def action_cancel_approval(self):
        for quote in self:
            quote.approval = False