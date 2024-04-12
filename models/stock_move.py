# -*- coding: utf-8 -*-
from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    material_production_id = fields.Many2one(
        'manufacture', 'Production Order for components')
    manufacturing_id = fields.Many2one('manufacture',
                                       string='Manufacturing Order')
