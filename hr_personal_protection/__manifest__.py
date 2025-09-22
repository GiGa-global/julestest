# -*- coding: utf-8 -*-
{
    'name': "HR Personal Protection",

    'summary': """
        Module for managing personal protection equipment for employees.""",

    'description': """
        This module adds functionality to manage and track the delivery of personal protection equipment to employees.
    """,

    'author': "Jules",
    'website': "https://www.odoo.com",

    'category': 'Human Resources',
    'version': '1.0',

    'depends': ['hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/personal_protection_element_views.xml',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': True,
}
