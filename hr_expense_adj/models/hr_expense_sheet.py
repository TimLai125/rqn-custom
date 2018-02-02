# -*- coding: utf-8 -*-
# Copyright 2017-2018 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    def _default_name(self):
        today = fields.Date.context_today(self)
        y, m, d = today.split('-')
        return y + '.' + m

    name = fields.Char(
        default=_default_name,
    )
    # change string of "submit" from "Submitted" to "To Be Approved"
    state = fields.Selection(
        [('submit', 'To Be Approved'),
         ('approve', 'Approved'),
         ('post', 'Posted'),
         ('done', 'Paid'),
         ('cancel', 'Refused')],
    )
    submitted = fields.Boolean(
        string='Submitted',
        compute='_update_submitted',
        store=True,
        readonly=True,
        default=False,
        copy=False,
    )
    # Overwrite default field definition
    expense_line_ids = fields.One2many('hr.expense', 'sheet_id',
                                       string='Expense Lines',
                                       states={'done': [('readonly', True)],
                                               'post': [('readonly', True)]},
                                       copy=False)

    def _assign_number(self, line):
        context = {'ir_sequence_date': line.date}
        line.number = self.env['ir.sequence'].with_context(context). \
            next_by_code('hr.expense')

    @api.model
    def create(self, vals):
        sheet = super(HrExpenseSheet, self).create(vals)
        for line in sheet.expense_line_ids.sorted(
                key=lambda x: (x.date, x.id)):
            self._assign_number(line)
        return sheet

    @api.multi
    def write(self, vals):
        res = super(HrExpenseSheet, self).write(vals)
        if self.state == 'submit':
            for line in self.expense_line_ids.sorted(
                    key=lambda x: (x.date, x.id)):
                if line.number == False:
                    self._assign_number(line)
            return res

    @api.multi
    def unlink(self):
        for line in self.expense_line_ids:
            line.number = False
        super(HrExpenseSheet, self).unlink()

    @api.multi
    def action_submit(self):
        for sheet in self:
            sheet.submitted = True

    @api.multi
    def action_cancel_submission(self):
        for sheet in self:
            sheet.submitted = False

    @api.multi
    @api.depends('state')
    def _update_submitted(self):
        for sheet in self:
            if sheet.state != 'submit':
                sheet.submitted = False
