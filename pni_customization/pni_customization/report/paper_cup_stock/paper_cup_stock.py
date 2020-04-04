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
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
        },
		{
            "fieldname": "size",
            "label": _("Cups in Stack"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "no_of_stack",
            "label": _("Stack in Carton"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "nos",
            "label": _("Nos"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "total",
            "label": _("Total Cup"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "net_weight",
            "label": _("Net Weight"),
            "fieldtype": "Float",
        },
        {
            "fieldname": "gross_weight",
            "label": _("Gross Weight"),
            "fieldtype": "Float",
        }
    ]

def get_data(filters=None):
    conditions = ""
    
    if filters.status:
        conditions += " and status = '{0}' ".format(filters.status)

    if filters.item:
        conditions += " and item = '{0}' ".format(filters.item)
    
    return frappe.db.sql("""
		
		select 
			item, status, size, no_of_stack, count(item), sum(total), sum(net_weight),
			sum(gross_weight)
		
		from 
			`tabPNI Carton` 
		
		where 
			docstatus = "1" and is_paper_plate = "" {0}
    	
		group by item,size,no_of_stack, status;
    """.format(conditions))