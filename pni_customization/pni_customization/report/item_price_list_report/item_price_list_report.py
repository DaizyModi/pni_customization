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
            "fieldname": "brand",
            "label": _("Brand"),
            "fieldtype": "Link",
            "options": "Brand",
            "width": 150
        },
		{
            "fieldname": "selling_rate",
            "label": _("Selling Rate"),
            "fieldtype": "Data",
            "width": 150,
			"precision":4
        },
		{
            "fieldname": "packing_rate",
            "label": _("Packing Rate"),
            "fieldtype": "Data",
            "width": 150,
			"precision":4
        },
		{
            "fieldname": "packing_rate_with_gst",
            "label": _("Packing Rate with GST"),
            "fieldtype": "Data",
            "width": 150,
			"precision":4
        },
		{
            "fieldname": "dumy",
            "label": _("Empty"),
            "fieldtype": "Data",
            "width": 150,
			"precision":4
        }

    ]

def get_data(filters=None):
	conditions = ""
	if filters.brand_group:
		conditions += " and bgt.parent = '{0}' ".format(filters.brand_group)
		
	conditions += get_condition()

	return frappe.db.sql("""
		select 
			ip.brand, ip.price_list_rate, (ip.price_list_rate * bg.multiplier) as decimal(10,4), (ip.price_list_rate * bg.multiplier * 1.18) as decimal(10,2)
		from 
			`tabItem Price` as ip,
			`tabBrand Group Table` as bgt,
			`tabBrand Group` as bg
		where 
			ip.customer is NULL
			and bgt.brand = ip.brand 
			and bg.name = bgt.parent
			{0}
		group by ip.brand
    """.format(conditions))

def get_condition():
	data = frappe.db.get_all("Brand Group", fields=['query', 'role'])
	query = ""
	user_roles = frappe.get_roles(frappe.session.user)
	print(user_roles)
	for group in data:
		print(group.role)
		if group.role and group.role in user_roles :
			query += group.query + ","
	if not query:
		frappe.throw("You DOn't have permission")
	return " and ip.brand in (" +query.strip(",") + ")"

