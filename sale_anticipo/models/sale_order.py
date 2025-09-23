# -*- coding: utf-8 -*-

from odoo import models, fields, api

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

    # This field tracks the last user input to resolve conflicts.
    # It's not meant to be shown in the UI.
    anticipo_source = fields.Selection(
        [('percent', 'Porcentaje'), ('amount', 'Monto')],
        string="Fuente del Anticipo"
    )

    @api.onchange('order_line')
    def _onchange_order_line(self):
        """
        Recalculates anticipo when order lines change.
        It respects the last input source.
        """
        if self.anticipo_source == 'percent':
            self._onchange_anticipo_porcentaje()
        elif self.anticipo_source == 'amount':
            self._onchange_monto_anticipo()

    @api.onchange('anticipo_porcentaje')
    def _onchange_anticipo_porcentaje(self):
        """
        Calculates amount from percentage.
        """
        if self.anticipo_porcentaje is not None:
            # To prevent this onchange from triggering the other one, we check if we are in an onchange context for monto_anticipo
            # A simpler way is to check if the value is what we expect
            expected_monto = self.amount_total * (self.anticipo_porcentaje / 100)
            if round(self.monto_anticipo, 2) != round(expected_monto, 2):
                self.monto_anticipo = expected_monto
                self.anticipo_source = 'percent'

    @api.onchange('monto_anticipo')
    def _onchange_monto_anticipo(self):
        """
        Calculates percentage from amount.
        """
        if self.monto_anticipo is not None and self.amount_total > 0:
            expected_porcentaje = (self.monto_anticipo / self.amount_total) * 100
            if round(self.anticipo_porcentaje, 2) != round(expected_porcentaje, 2):
                self.anticipo_porcentaje = expected_porcentaje
                self.anticipo_source = 'amount'
        elif self.amount_total == 0 and self.monto_anticipo != 0:
            self.anticipo_porcentaje = 0.0
            self.anticipo_source = 'amount'
