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
        }
    ]

def get_data(filters=None):
	conditions = ""
	join = ""
	if filters.brand_group:
		conditions += " and bgt.brand = ip.brand "
		join += " ,`tabBrand Group Table` as bgt"
		conditions += " and bgt.parent = '{0}' ".format(filters.brand_group)
		
	conditions += get_condition()

	return frappe.db.sql("""
		select 
			ip.brand,ip.price_list_rate
		from 
			`tabItem Price` as ip
			{1}
		where 
			ip.customer = ""
			{0}
		group by ip.brand
    """.format(conditions, join))

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

