# -*- coding: utf-8 -*-
{
    'name': "Sale Anticipo",

    'summary': """
        Agrega campos de anticipo en la orden de venta.""",

    'description': """
        Este módulo agrega un campo de porcentaje de anticipo y el monto del anticipo calculado en la orden de venta.
    """,

    'author': "GiGa global SG15",
    'website': "https://www.gigaglobal.com.ar",

    'category': 'Sales',
    'version': '18.0.0.5',

    'depends': ['sale_management'],

    'data': [
        'views/sale_order_view.xml',
    ],
}
