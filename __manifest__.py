{
    "name": "Peepl - Helpdesk",
    "version": "19.0.0.0.0",
    "category": "Additional Tools",
    "summary": "Helpdesk customization for Peepl",
    "description": "This module provides customizations for the Helpdesk application in Odoo, tailored to meet the specific needs of Peepl. It includes features such as user-wise menu hiding and other enhancements to improve the user experience and efficiency of the Helpdesk system.",
    "depends": ["base", "helpdesk"],
    "data": [
        "security/ir.model.access.csv",
        "views/helpdesk_classification_views.xml",
        "views/helpdesk_classification_actions.xml",
        "views/helpdesk_classification_menu.xml",
        "views/helpdesk_sla_form.xml",
        "views/helpdesk_ticket_list.xml",
        "views/helpdesk_ticket_form.xml",
    ],

    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
    "external_dependencies": {},
    "application": False,
}
