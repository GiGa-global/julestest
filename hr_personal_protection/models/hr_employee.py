# -*- coding: utf-8 -*-

from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    protection_element_ids = fields.One2many('employee.protection.element', 'employee_id', string='Protection Elements')
