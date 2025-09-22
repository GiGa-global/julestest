# -*- coding: utf-8 -*-

from odoo import models, fields

class PersonalProtectionElement(models.Model):
    _name = 'personal.protection.element'
    _description = 'Personal Protection Element'

    name = fields.Char(string='Name', required=True)
    type = fields.Char(string='Type')
    usage = fields.Text(string='Usage')
    standard = fields.Char(string='Standard')
