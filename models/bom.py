# -*- coding: utf-8 -*-
from odoo import fields, models


class Bom(models.Model):
    """manage bom"""
    _name = 'bom'
    _rec_name = 'product_tmpl_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bill Of Material'

    product_tmpl_id = fields.Many2one(
        'product.template', required=True, string='Product')
    product_qty = fields.Float(
        'Quantity', default=1.0)
    company_id = fields.Many2one(
        'res.company', 'Company', index=True,
        default=lambda self: self.env.company)
    bom_new_line_ids = fields.One2many('bom.new.line',
                                       'bom_id',
                                       'BoM Lines', copy=True)
    product_id = fields.Many2one('product.product', string='Product')
