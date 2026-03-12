from odoo import fields, models, api
from datetime import datetime


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    deadline = fields.Datetime(
        string="Deadline",
        help="Deadline for resolving this ticket"
    )
    category_id = fields.Many2one(
        "helpdesk.category",
        string="Category"
    )
    subcategory_id = fields.Many2one(
        "helpdesk.subcategory",
        string="Sub Category",
        domain="[('category_id', '=', category_id)]"
    )
    item_id = fields.Many2one(
        "helpdesk.item",
        string="Item",
        domain="[('subcategory_id', '=', subcategory_id)]"
    )

    @api.onchange('deadline', 'team_id')
    def _onchange_deadline_update_priority(self):
        """Auto-update priority when deadline changes based on SLA auto_priority setting"""
        if not self.deadline or not self.team_id:
            return

        # Get SLA policies for this team with auto_priority enabled
        sla_policies = self.env['helpdesk.sla'].search([
            ('team_id', '=', self.team_id.id),
            ('auto_priority', '=', True),
            ('active', '=', True)
        ])

        if not sla_policies:
            return

        # Use first matching SLA policy
        sla = sla_policies[0]
        now = datetime.now()
        time_remaining = (self.deadline - now).total_seconds() / 3600

        # Priority mapping: '0'=Low, '1'=Medium, '2'=High, '3'=Urgent
        if time_remaining <= sla.priority_threshold_urgent:
            self.priority = '3'  # Urgent
        elif time_remaining <= sla.priority_threshold_high:
            self.priority = '2'  # High
        elif time_remaining <= sla.priority_threshold_medium:
            self.priority = '1'  # Medium
        elif time_remaining > sla.priority_threshold_low:
            self.priority = '0'  # Low
