# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_is_zero

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    anticipo_porcentaje = fields.Float(
        string='Anticipo %',
        digits='Discount',
    )

    monto_anticipo = fields.Monetary(
        string='Monto Anticipo',
        currency_field='currency_id',
    )

    @api.onchange('anticipo_porcentaje')
    def _onchange_anticipo_porcentaje(self):
        """
        Calculates the amount when the percentage is changed.
        The check on the existing value prevents recursion.
        """
        # This guard is to prevent the onchange from running in a loop.
        # We check if the expected value is already set.
        if self.anticipo_porcentaje is not None:
            expected_monto = self.amount_total * (self.anticipo_porcentaje / 100)
            if not float_is_zero(self.monto_anticipo - expected_monto, precision_digits=2):
                self.monto_anticipo = expected_monto

    @api.onchange('monto_anticipo')
    def _onchange_monto_anticipo(self):
        """
        Calculates the percentage when the amount is changed.
        The check on the existing value prevents recursion.
        """
        if self.monto_anticipo is not None:
            if self.amount_total > 0:
                expected_porcentaje = (self.monto_anticipo / self.amount_total) * 100
                if not float_is_zero(self.anticipo_porcentaje - expected_porcentaje, precision_digits=2):
                    self.anticipo_porcentaje = expected_porcentaje
            else:
                self.anticipo_porcentaje = 0.0

    @api.onchange('amount_total')
    def _onchange_amount_total(self):
        """
        Recalculates the down payment amount if the order total changes,
        respecting the percentage as the source of truth.
        """
        if self.anticipo_porcentaje is not None:
            self.monto_anticipo = self.amount_total * (self.anticipo_porcentaje / 100)