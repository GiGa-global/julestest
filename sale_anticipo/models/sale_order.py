# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # --- Down Payment Calculation Fields ---
    # Using the robust compute/inverse pattern with a stored "source of truth" field.

    # This is the raw stored value, not shown on the UI.
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

    # --- Dynamic Note Field for Report ---
    # This field is computed only for the report and does not replace the editable 'note' field in the form view.

    note_for_report = fields.Html(
        string='Nota para Reporte',
        compute='_compute_note_for_report',
        store=False, # No need to store, computed on the fly for printing.
    )

    # --- Compute / Inverse Methods ---

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
                order.monto_anticipo = 0.0

    def _inverse_monto_anticipo(self):
        for order in self:
            if order.amount_total > 0 and order.monto_anticipo > 0:
                order.anticipo_porcentaje_fijo = (order.monto_anticipo / order.amount_total) * 100
            else:
                order.anticipo_porcentaje_fijo = 0.0

    @api.depends('note', 'monto_anticipo', 'currency_id')
    def _compute_note_for_report(self):
        for order in self:
            if order.note:
                amount_text = f"{order.monto_anticipo:,.2f}"
                if order.currency_id:
                    amount_text = f"{order.currency_id.symbol} {amount_text}"
                order.note_for_report = order.note.replace('$Monto', amount_text)
            else:
                order.note_for_report = False
