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
            "width": 150
        },
		{
            "fieldname": "brand",
            "label": _("Brand"),
            "fieldtype": "Link",
            "options": "Brand",
            "width": 150
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
        },
		{
            "fieldname": "actual_stock",
            "label": _("Actual Stock"),
            "fieldtype": "Float",
			"width": 100
        }
    ]

def get_data(filters=None):
	conditions = ""

	if filters.status:
		conditions += " and crt.status = '{0}' ".format(filters.status)

	if filters.item:
		conditions += " and crt.item = '{0}' ".format(filters.item)
	
	if filters.brand:
		conditions += " and item.brand = '{0}' ".format(filters.brand)

	if filters.from_date:
		conditions += " and crt.creation >= '{0}' ".format(filters.from_date)
	
	if filters.to_date:
		conditions += " and crt.creation <='{0}' ".format(filters.to_date)

	return frappe.db.sql("""
		select 
			crt.item, crt.brand, crt.status, crt.size, crt.no_of_stack, crt.nos, crt.total, crt.net_weight,
			crt.gross_weight, sum(bin.actual_qty)
		
		from 
			(select 
				crt.item, item.brand, crt.status, crt.size, crt.no_of_stack, count(crt.item) as nos, sum(crt.total) as total, sum(crt.net_weight) as net_weight,
				sum(crt.gross_weight) as gross_weight
			
			from 
				`tabItem` as item, `tabPNI Carton` as crt
			
			where 
				item.name = crt.item and
				crt.docstatus = "1" and crt.is_paper_plate = "" {0}
			
			group by crt.item,crt.size,crt.no_of_stack, crt.status) as crt

		left join
			`tabBin` as bin
		on bin.item_code = crt.item 
		group by crt.item	
    """.format(conditions))