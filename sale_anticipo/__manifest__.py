# -*- coding: utf-8 -*-
{
    'name': "Sale Anticipo",

    'summary': """
        Agrega campos de anticipo en la orden de venta.""",

    'description': """
        Este módulo agrega un campo de porcentaje de anticipo y el monto del anticipo calculado en la orden de venta.
    """,

    'author': "Jules",
    'website': "https://www.example.com",

    'category': 'Sales',
    'version': '1.0',

    'depends': ['sale_management'],

    'data': [
        'views/sale_order_view.xml',
        'views/sale_report_templates.xml',
    ],
}
