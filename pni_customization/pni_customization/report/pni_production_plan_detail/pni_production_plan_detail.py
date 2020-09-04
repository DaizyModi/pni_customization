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
            "fieldname": "sales_order",
            "label": _("Sales Order"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 180
        },
		{
            "fieldname": "date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 180
        },
		{
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 180
        },
		{
            "fieldname": "sales_person",
            "label": _("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 180
        },
		{
            "fieldname": "order_qty",
            "label": _("Order Qty"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "delivery_qty",
            "label": _("Deliver Qty"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "pending_qty",
            "label": _("Pending Qty"),
            "fieldtype": "Float",
			"width": 100
        },
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
            "fieldname": "projected_qty",
            "label": _("Projected Qty"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "projected_box",
            "label": _("Projected Box"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "actual_qty",
            "label": _("Actual Qty"),
            "fieldtype": "Float",
			"width": 100
        },
		{
            "fieldname": "actual_box",
            "label": _("Actual Box"),
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
			result3.so_name, so.transaction_date, so.customer_name, st.sales_person,result3.qty,result3.delivered_qty,result3.pending_qty,
			result3.warehouse, result3.item_code, 
			result3.projected_qty,result3.box,
			result3.actual_qty, result3.actual_box, result3.ordered_qty, 
			result3.planned_qty, result3.reserved_qty, 
			result3.item_name, result3.description
		from 
			(
				select 
					soi.parent as so_name, soi.qty,soi.delivered_qty,(soi.qty-soi.delivered_qty) as pending_qty,
					result2.warehouse, result2.item_code, 
					result2.projected_qty,result2.box,
					result2.actual_qty, result2.actual_box, result2.ordered_qty, 
					result2.planned_qty, result2.reserved_qty, 
					result2.item_name, result2.description
				from (
					select 
						result.warehouse, result.item_code, result.actual_qty, 
						result.ordered_qty, result.planned_qty ,
						result.reserved_qty, result.projected_qty,
						(result.projected_qty / NULLIF(uom_con.conversion_factor,1)) as box, 
						(result.actual_qty / NULLIF(uom_con.conversion_factor,1)) as actual_box, 
						result.item_name, result.description
					from 
						(
							SELECT  
								bin.warehouse, bin.item_code, bin.actual_qty, 
								bin.ordered_qty, bin.planned_qty ,
								bin.reserved_qty, bin.projected_qty, 
								item.item_name, item.description
							FROM 
								tabBin as bin
							INNER JOIN 
								tabItem as item
							ON 	bin.item_code=item.name
							WHERE 	bin.projected_qty<0  {0}
							ORDER BY 	bin.projected_qty
						) as result
					Left JOIN
						`tabUOM Conversion Detail` as uom_con
					ON
						uom_con.parent = result.item_code and uom_con.uom = "Box" 
				) as result2
				LEFT JOIN
					`tabSales Order Item` as soi
				ON
					soi.item_code = result2.item_code 
					and soi.docstatus= 1 
					and soi.qty <> soi.delivered_qty
			) as result3
		LEFT JOIN
			`tabSales Order` as so
		ON
			so.name = result3.so_name and so.status <> "Closed"
		LEFT JOIN
			`tabSales Team` as st
		ON
			st.parent = result3.so_name
	""".format(conditions))