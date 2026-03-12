from odoo import fields, models


class HelpdeskCategory(models.Model):
    _name = "helpdesk.category"
    _description = "Helpdesk Category"
    _order = "sequence, name"

    name = fields.Char(string="Category Name", required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    description = fields.Text()


class HelpdeskSubCategory(models.Model):
    _name = "helpdesk.subcategory"
    _description = "Helpdesk Sub Category"
    _order = "sequence, name"

    name = fields.Char(string="Sub Category Name", required=True)
    category_id = fields.Many2one(
        "helpdesk.category",
        string="Category",
        required=True,
        ondelete="cascade"
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    description = fields.Text()


class HelpdeskItem(models.Model):
    _name = "helpdesk.item"
    _description = "Helpdesk Item"
    _order = "sequence, name"

    name = fields.Char(string="Item Name", required=True)
    subcategory_id = fields.Many2one(
        "helpdesk.subcategory",
        string="Sub Category",
        required=True,
        ondelete="cascade"
    )
    category_id = fields.Many2one(
        "helpdesk.category",
        string="Category",
        related="subcategory_id.category_id",
        store=True,
        readonly=True
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    description = fields.Text()
