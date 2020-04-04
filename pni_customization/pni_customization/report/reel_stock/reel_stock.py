# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    data = get_data(filters)
    columns = get_columns()
    return columns, data

def get_columns():
    return  [
        {
            "fieldname": "item",
            "label": _("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 300
        },
        {
            "fieldname": "nos",
            "label": _("Nos"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "total_weight",
            "label": _("Total Weight"),
            "fieldtype": "Float",
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "size",
            "label": _("Size"),
            "fieldtype": "Float",
        },
        {
            "fieldname": "gsm",
            "label": _("GSM"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "brand",
            "label": _("Brand"),
            "fieldtype": "Link",
            "options": "Brand"
        },
        {
            "fieldname": "coated_reel",
            "label": _("Coated Reel"),
            "fieldtype": "Check",
        },
        {
            "fieldname": "printed_reel",
            "label": _("Printed Reel"),
            "fieldtype": "Check",
        }
    ]

def get_data(filters=None):
    conditions = ""
    
    if filters.status:
        conditions += " and status = '{0}' ".format(filters.status)

    if filters.item:
        conditions += " and item = '{0}' ".format(filters.item)
    
    if filters.brand:
        conditions += " and brand = '{0}' ".format(filters.brand)
    
    if filters.gsm:
        conditions += " and gsm = '{0}' ".format(filters.gsm)
    
    if filters.size:
        conditions += " and size = '{0}' ".format(filters.sizes)
    
    if filters.coated:
        conditions += " and coated_reel = '{0}' ".format(filters.coated)
    
    if filters.printed:
        conditions += " and printed_reel = '{0}' ".format(filters.printed)
    
    return frappe.db.sql("""
            select 
                item, count(item), sum(weight), status, size, gsm, brand, 
                coated_reel, printed_reel

            from `tabReel` 
                where docstatus = '1' {0}

            group by 
                item, size, gsm, coated_reel, printed_reel;
        """.format(conditions))