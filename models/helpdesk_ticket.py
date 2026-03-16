from odoo import fields, models, api
from datetime import datetime


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    is_draft = fields.Boolean(string="Is Draft", default=False, copy=False)
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
    opened_by_id = fields.Many2one(
        "res.users",
        string="Opened By",
        compute="_compute_opened_by",
        store=True,
        readonly=True
    )

    @api.depends('create_uid')
    def _compute_opened_by(self):
        for rec in self:
            rec.opened_by_id = rec.create_uid

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

    def _compute_priority_from_deadline(self):
        for rec in self:
            if not rec.deadline or not rec.team_id:
                continue
            sla = self.env['helpdesk.sla'].search([
                ('team_id', '=', rec.team_id.id),
                ('auto_priority', '=', True),
                ('active', '=', True)
            ], limit=1)
            if not sla:
                continue
            time_remaining = (rec.deadline - datetime.now()).total_seconds() / 3600
            if time_remaining <= sla.priority_threshold_urgent:
                rec.priority = '3'
            elif time_remaining <= sla.priority_threshold_high:
                rec.priority = '2'
            elif time_remaining <= sla.priority_threshold_medium:
                rec.priority = '1'
            else:
                rec.priority = '0'

    @api.model_create_multi
    def create(self, vals_list):
        draft_indices = [i for i, v in enumerate(vals_list) if v.get('is_draft')]
        for i in draft_indices:
            vals_list[i]['stage_id'] = False
        tickets = super().create(vals_list)
        draft_tickets = tickets.filtered('is_draft')
        if draft_tickets:
            seq = self.env['ir.sequence'].sudo().search([('code', '=', 'helpdesk.ticket')], limit=1)
            if seq:
                seq.number_next_actual -= len(draft_tickets)
            draft_tickets.sudo().write({'ticket_ref': False})
        tickets._compute_priority_from_deadline()
        return tickets

    def write(self, vals):
        res = super().write(vals)
        if 'deadline' in vals or 'team_id' in vals:
            self._compute_priority_from_deadline()
        return res

    def action_save_as_draft(self):
        self.ensure_one()
        self.write({'is_draft': True, 'ticket_ref': False, 'stage_id': False})

    def action_submit(self):
        self.ensure_one()
        team = self.team_id
        stage = team._determine_stage()[team.id] if team else self.env['helpdesk.stage'].search([], limit=1)
        company = team.company_id if team else self.env.company
        ticket_ref = self.env['ir.sequence'].with_company(company).sudo().next_by_code('helpdesk.ticket')
        self.write({
            'is_draft': False,
            'ticket_ref': ticket_ref,
            'stage_id': stage.id,
        })

