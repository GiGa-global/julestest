# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # This is the raw stored value (source of truth), set by the user via one of the computed fields below.
    anticipo_porcentaje_fijo = fields.Float(
        string='Porcentaje de Anticipo Fijo',
        digits='Discount',
        copy=True
    )

    # Computed field for user interaction (Percentage)
    anticipo_porcentaje = fields.Float(
        string='Anticipo %',
        compute='_compute_anticipo_porcentaje',
        inverse='_inverse_anticipo_porcentaje',
        store=True,
        readonly=False,
        digits='Discount',
    )

    # Computed field for user interaction (Amount)
    monto_anticipo = fields.Monetary(
        string='Monto Anticipo',
        compute='_compute_monto_anticipo',
        inverse='_inverse_monto_anticipo',
        store=True,
        readonly=False,
        currency_field='currency_id',
    )

    @api.depends('anticipo_porcentaje_fijo')
    def _compute_anticipo_porcentaje(self):
        for order in self:
            order.anticipo_porcentaje = order.anticipo_porcentaje_fijo

    def _inverse_anticipo_porcentaje(self):
        for order in self:
            order.anticipo_porcentaje_fijo = order.anticipo_porcentaje

    @api.depends('amount_total', 'anticipo_porcentaje_fijo')
    def _compute_monto_anticipo(self):
        for order in self:
            if order.anticipo_porcentaje_fijo > 0:
                order.monto_anticipo = order.amount_total * (order.anticipo_porcentaje_fijo / 100)
            else:
                # If monto_anticipo was set manually, this would overwrite it.
                # The inverse method on monto_anticipo should be the only way to set a value that
                # is not based on the percentage.
                # The logic holds: the percentage is the source of truth.
                order.monto_anticipo = 0.0

    def _inverse_monto_anticipo(self):
        for order in self:
            if order.amount_total > 0 and order.monto_anticipo > 0:
                order.anticipo_porcentaje_fijo = (order.monto_anticipo / order.amount_total) * 100
            else:
                order.anticipo_porcentaje_fijo = 0.0

    # --- Dynamic Terms & Conditions ---

    note_dinamico = fields.Html(
        string='Términos y Condiciones Dinámicos',
        compute='_compute_note_dinamico',
        store=False, # This should not be stored, it's always computed on the fly
    )

    @api.depends('note', 'monto_anticipo', 'currency_id')
    def _compute_note_dinamico(self):
        for order in self:
            if order.note:
                # Format the amount with currency
                amount_text = f"{order.currency_id.symbol} {order.monto_anticipo:,.2f}"
                order.note_dinamico = order.note.replace('$Monto', amount_text)
            else:
                order.note_dinamico = False
