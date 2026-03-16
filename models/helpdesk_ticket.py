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
    item_category_id = fields.Many2one(
        "helpdesk.item.category",
        string="Item Category",
        domain="[('subcategory_id', '=', subcategory_id)]"
    )
    item_id = fields.Many2one(
        "helpdesk.item",
        string="Item",
        domain="[('item_category_id', '=', item_category_id)]"
    )
    has_auto_priority = fields.Boolean(
        compute="_compute_has_auto_priority",
        store=False
    )

    @api.depends('team_id')
    def _compute_has_auto_priority(self):
        for rec in self:
            rec.has_auto_priority = bool(self.env['helpdesk.sla'].search([
                ('team_id', '=', rec.team_id.id),
                ('auto_priority', '=', True),
                ('active', '=', True)
            ], limit=1))

    @api.onchange('category_id')
    def _onchange_category_id(self):
        self.subcategory_id = False
        self.item_category_id = False
        self.item_id = False

    @api.onchange('subcategory_id')
    def _onchange_subcategory_id(self):
        self.item_category_id = False
        self.item_id = False

    @api.onchange('item_category_id')
    def _onchange_item_category_id(self):
        self.item_id = False

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
