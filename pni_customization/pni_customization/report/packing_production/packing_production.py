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
            "fieldname": "machine_helper",
            "label": _("Machine Helper"),
            "fieldtype": "Data",
            "width": 150
        },
		{
            "fieldname": "shift",
            "label": _("Shift"),
            "fieldtype": "Data",
            "width": 150,
			"precision":4
        },
		{
            "fieldname": "total_stock",
            "label": _("Total Stock"),
            "fieldtype": "Float",
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
	if filters.from_date:
		conditions += " and date >= '{0}' ".format(filters.from_date)
	
	if filters.to_date:
		conditions += " and date <='{0}' ".format(filters.to_date)
	

	return frappe.db.sql("""
		select 
			machine_helper,
			shift,
			sum(total_shift_stock)
		from
			`tabPNI Packing`
		where
			docstatus = 1 {0}
		group by 
			machine_helper,shift;
    """.format(conditions))