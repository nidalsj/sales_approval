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


    def _notify_sales_approvers(self, message):
        group = self.env.ref('sales_approval.om_group_sales_approver')
        users = group.users
        if users:
            notification_ids = [(0, 0,
                                {
                                    'res_partner_id': user.partner_id.id,
                                    'notification_type': 'inbox'
                                }
                                ) for user in users if users]
            self.env['mail.message'].create({
            'message_type': "notification",
            'body': message,
            'subject': "Sale Order",
            'partner_ids': [(4, user.partner_id.id) for user in users if users],
            'model': self._name,
            'res_id': self.id,
            'notification_ids': notification_ids,
            'author_id': self.env.user.partner_id and self.env.user.partner_id.id
        })

    
    def action_submit(self):
        if not self.env.user.has_group('sales_approval.om_group_sales_approver'):
            raise UserError('You do not have the rights to perform this action.')
        self.write({'state': 'waiting_approval'})
        self._notify_sales_approvers("Sale order %s submitted for approval" % (self.name))


    def action_approve(self):
        if not self.env.user.has_group('sales_approval.om_group_sales_approver'):
            raise UserError('You do not have the rights to perform this action.')
        self.write({'state': 'approved'})
        self._notify_sales_approvers("Sale order %s is approved" % (self.name))


    def action_reject(self):
        if not self.env.user.has_group('sales_approval.om_group_sales_approver'):
            raise UserError('You do not have the rights to perform this action.')
        self.write({'state': 'draft'})
        self._notify_sales_approvers("Sale order %s is rejected" % (self.name))


    def action_confirm(self):
        if not self.env.user.has_group('sales_approval.om_group_sales_approver'):
            raise UserError('You do not have the rights to perform this action.')
        if self.state != 'approved':
            raise UserError('Invalid Operation: The sale order must be approved before it can be confirmed.')
        super(SaleOrder, self).action_confirm()
        self._notify_sales_approvers("Sale order %s confirmed" % (self.name))
    

    # override and allow confirmation from approved state
    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent', 'approved'}
    