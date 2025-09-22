# -*- coding: utf-8 -*-

from odoo import models, fields

class EmployeeProtectionElement(models.Model):
    _name = 'employee.protection.element'
    _description = 'Employee Protection Element'

    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    element_id = fields.Many2one('personal.protection.element', string='Protection Element', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
