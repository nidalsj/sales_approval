from odoo import models, fields, api
from odoo.exceptions import UserError

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

    
    def action_submit(self):
        self.message_post(body="Sale order submitted for approval by %s" % (self.env.user.name))
        self.write({'state': 'waiting_approval'})

    def action_approve(self):
        self.message_post(body="Sale order approved by %s" % (self.env.user.name))
        self.write({'state': 'approved'})

    def action_reject(self):
        self.message_post(body="Sale order rejected by %s" % (self.env.user.name))
        self.write({'state': 'draft'})

    def action_confirm(self):
        if self.state != 'approved':
            raise UserError('Invalid Operation: The sale order must be approved before it can be confirmed.')
        self.message_post(body="Sale order confirmed by %s" % (self.env.user.name))
        super(SaleOrder, self).action_confirm()


    # override and allow confirmation from approved state
    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent', 'approved'}
    
    