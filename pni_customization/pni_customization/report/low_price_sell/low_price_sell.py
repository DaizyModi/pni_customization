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
            "width": 150
        },
		{
            "fieldname": "title",
            "label": _("Title"),
            "fieldtype": "Data",
            "width": 150
        },
		{
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
			"options": "Customer"
        },
		{
            "fieldname": "date",
            "label": _("Date"),
            "fieldtype": "Date",
        },
        {
            "fieldname": "item",
            "label": _("Item"),
            "fieldtype": "Link",
			"options": "Item"
        },
        {
            "fieldname": "price_list_rate",
            "label": _("Price List Rate"),
            "fieldtype": "Float",
        },
        {
            "fieldname": "sell_rate",
            "label": _("Sell Rate"),
            "fieldtype": "Float",
        },
        {
            "fieldname": "diff",
            "label": _("Difference"),
            "fieldtype": "Float",
        },
		{
            "fieldname": "diff_in_per",
            "label": _("Difference in Percentage"),
            "fieldtype": "Float",
        }
    ]

def get_data(filters=None):
	conditions = ""
	table_join = ""

	if filters.from_date:
		conditions += " and so.creation >= '{0}' ".format(filters.from_date)
	
	if filters.to_date:
		conditions += " and so.creation <='{0}' ".format(filters.to_date)
	
	if filters.item_group:
		conditions += " and item.name = soi.item_code and item.item_group = '{0}' ".format(filters.item_group)
		table_join += ", `tabItem` as item "

	return frappe.db.sql("""
		select 
			so.name, so.title, so.customer, so.transaction_date, soi.item_code,
			soi.price_list_rate, soi.rate, 	(soi.price_list_rate - soi.rate) as diff, 
			((soi.price_list_rate - soi.rate)*100/soi.price_list_rate) as diff_per
		from 
			 `tabSales Order` as so, `tabSales Order Item` as soi
				{1}
		where 
			so.name = soi.parent and
			so.docstatus <> "2" and
			soi.price_list_rate > soi.rate and
			soi.approve_law_rate__ <> "1"
			{0};
    """.format(conditions, table_join))
