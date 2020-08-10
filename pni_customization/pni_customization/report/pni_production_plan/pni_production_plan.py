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
            "fieldname": "warehouse",
            "label": _("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 180
        },
		{
            "fieldname": "item_code",
            "label": _("Item"),
            "fieldtype": "Link",
			"options": "Item",
            "width": 150
        },
		{
            "fieldname": "actual_qty",
            "label": _("Actual Qty"),
            "fieldtype": "Float",
			"width": 100
        },
        {
            "fieldname": "ordered_qty",
            "label": _("Ordered Qty"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "planned_qty",
            "label": _("Planned Qty"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "reserved_qty",
            "label": _("Reserved Qty"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "projected_qty",
            "label": _("Projected Qty"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "box",
            "label": _("Box"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
			"width": 100
        },
		{
            "fieldname": "description",
            "label": _("Description"),
            "fieldtype": "Data",
			"width": 100
        }
    ]

def get_data(filters=None):
	conditions = ""
	if filters.warehouse:
		conditions += " and bin.warehouse = '{0}' ".format(filters.warehouse)
	
	return frappe.db.sql("""
		select 
			result.warehouse, result.item_code, result.actual_qty, result.ordered_qty, result.planned_qty ,
			result.reserved_qty, result.projected_qty,result.projected_qty / NULLIF(uom_con.conversion_factor,1), 
			result.item_name, result.description
			from 
				(SELECT  
					bin.warehouse, bin.item_code, bin.actual_qty, bin.ordered_qty, bin.planned_qty ,
					bin.reserved_qty, bin.projected_qty, item.item_name, item.description
				FROM 
					tabBin as bin
				INNER JOIN 
					tabItem as item
				ON 	bin.item_code=item.name
				WHERE 	bin.projected_qty<0  {0}
				ORDER BY 	bin.projected_qty) as result
			Left JOIN
				`tabUOM Conversion Detail` as uom_con
			ON
				uom_con.parent = result.item_code and uom_con.uom = "Box" 


	""".format(conditions))