# -*- coding: utf-8 -*-
from odoo import fields, models


class BomNewLine(models.Model):
    _name = 'bom.new.line'
    _description = 'Bill of Material Line'

    product_id = fields.Many2one('product.product', 'Component', required=True,
                                 check_company=True)
    company_id = fields.Many2one(
        related='bom_id.company_id', store=True, index=True, readonly=True)
    product_qty = fields.Float(
        'Quantity', default=1.0)
    bom_id = fields.Many2one('bom', string='Parent BoM')





    # product_tmpl_id = fields.Many2one('product.template', 'Product Template',
    #                                   related='product_id.product_tmpl_id',
    #                                   store=True)
