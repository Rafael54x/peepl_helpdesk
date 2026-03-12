from odoo import fields, models, api
from datetime import datetime


class HelpdeskSLA(models.Model):
    _inherit = "helpdesk.sla"

    auto_priority = fields.Boolean(
        string="Auto Set Priority",
        default=False,
        help="Automatically set ticket priority based on time remaining to deadline"
    )
    priority_threshold_low = fields.Float(
        string="Low Priority Threshold (hours)",
        default=48.0,
        help="If time remaining is greater than this, set priority to Low"
    )
    priority_threshold_medium = fields.Float(
        string="Medium Priority Threshold (hours)",
        default=24.0,
        help="If time remaining is between Medium and High threshold, set priority to Medium"
    )
    priority_threshold_high = fields.Float(
        string="High Priority Threshold (hours)",
        default=4.0,
        help="If time remaining is between High and Urgent threshold, set priority to High"
    )
    priority_threshold_urgent = fields.Float(
        string="Urgent Priority Threshold (hours)",
        default=1.0,
        help="If time remaining is less than this, set priority to Urgent"
    )
