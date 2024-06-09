from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[
            ('waiting_approval', 'Waiting Approval'),
            ('approved', 'Approved'),('sale',)
        ],
        string='State'
    )

    def action_submit(self):
        self.write({'state': 'waiting_approval'})


    def action_approve(self):
        self.write({'state': 'approved'})


    def action_reject(self):
        self.write({'state': 'draft'})


    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent', 'approved'}
    
    