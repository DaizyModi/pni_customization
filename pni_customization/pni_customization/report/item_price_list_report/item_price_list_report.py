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
            "fieldtype": "Currency",
            "width": 150
        }
    ]

def get_data(filters=None):
	conditions = ""
	if filters.from_date:
		conditions += " and so.transaction_date >= '{0}' ".format(filters.from_date)
	conditions += get_condition()
	print("""
		select 
			brand,price_list_rate
		from 
			 `tabItem Price`
		where 
			1=1
			{0}
		group by brand
    """.format(conditions))
	return frappe.db.sql("""
		select 
			brand,price_list_rate
		from 
			 `tabItem Price`
		where 
			1=1
			{0}
		group by brand
    """.format(conditions))

def get_condition():
	data = frappe.db.get_all("Brand Group", fields=['query', 'role'])
	query = ""
	user_roles = frappe.get_roles(frappe.session.user)
	print(user_roles)
	for group in data:
		print(group.role)
		if group.role and group.role in user_roles :
			query += group.query

	return " and brand in (" +query + ")"

