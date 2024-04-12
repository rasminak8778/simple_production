# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Manufacture(models.Model):
    _name = "manufacture"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'product_id'

    product_id = fields.Many2one(
        'product.product', string='Product', required=True)
    product_tmpl_id = fields.Many2one('product.template',
                                      'Product Template',
                                      related='product_id.product_tmpl_id')
    product_qty = fields.Float(string='Quantity', copy=False, default=1.0)
    bom_id = fields.Many2one(
        'bom', string='Bill of Material', readonly=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')], string='State', copy=False,
        index=True, readonly=True,
        store=True, tracking=True)
    move_raw_material_ids = fields.One2many(
        'stock.move', 'material_production_id',
        'Components',
        readonly=False,
        copy=False)

    move_product_id = fields.Many2one('stock.move',
                                      sting='Product Move Details')

    def create_transfer_moves(self):
        """Function defined for creating product moves in Manufacturing"""
        moves = []
        move_vals = {
            'name': self.product_id.display_name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.product_qty,
            'quantity': self.product_qty,
            'location_id': self.env.
            ref('simple_production.manufacture_location').id,
            'location_dest_id': self.env.
            ref('stock.stock_location_stock').id,
            'state': 'done',
            'manufacturing_id': self.id,
        }
        moves.append(move_vals)
        for line in self.move_raw_material_ids:
            move_vals = {
                'name': line.product_id.display_name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'quantity': line.quantity,
                'location_id': self.env.
                ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.
                ref('simple_production.manufacture_location').id,
                'state': 'done',
                'manufacturing_id': self.id,
            }
            moves.append(move_vals)
        print('sss', moves)
        move = self.env['stock.move'].create(moves)
        for record in move:
            record._action_assign()
            record._action_done()

    def action_confirm_manufacture(self):
        """Function defined for confirm button"""
        self.state = 'confirmed'
        self.create_transfer_moves()

    def action_view_moves(self):
        """Function defined for Smart button view product moves"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'manufacture stock picking',
            'view_mode': 'tree,form',
            'res_model': 'stock.move',
            'context': "{'create': False}",
            'domain': [('manufacturing_id', '=', self.id)],
        }

    @api.onchange('bom_id')
    def onchange_bom_id(self):
        """function for Updating the manufacturing order by giving BoM"""
        if self.bom_id:
            self.product_id = self.bom_id.product_tmpl_id.product_variant_id.id
            self.product_qty = self.bom_id.product_qty
        for rec in self.bom_id.bom_new_line_ids:
            location_dest_id = self.env.ref(
                'simple_production.manufacture_location').id
            self.update({
                'move_raw_material_ids': [(fields.Command.create({
                    'product_id': rec.product_id.id,
                    'quantity': rec.product_qty,
                    'location_id': self.env.ref(
                                        'stock.stock_location_stock').id,
                    'location_dest_id': location_dest_id,
                    'name': 'line'
                }))]
            })
