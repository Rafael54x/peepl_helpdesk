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


class HelpdeskItemCategory(models.Model):
    _name = "helpdesk.item.category"
    _description = "Helpdesk Item Category"
    _order = "sequence, name"

    name = fields.Char(string="Item Category Name", required=True)
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


class HelpdeskItem(models.Model):
    _name = "helpdesk.item"
    _description = "Helpdesk Item"
    _order = "sequence, name"

    name = fields.Char(string="Item Name", required=True)
    item_category_id = fields.Many2one(
        "helpdesk.item.category",
        string="Item Category",
        required=True,
        ondelete="cascade"
    )
    subcategory_id = fields.Many2one(
        "helpdesk.subcategory",
        string="Sub Category",
        related="item_category_id.subcategory_id",
        store=True,
        readonly=True
    )
    category_id = fields.Many2one(
        "helpdesk.category",
        string="Category",
        related="item_category_id.category_id",
        store=True,
        readonly=True
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    description = fields.Text()
