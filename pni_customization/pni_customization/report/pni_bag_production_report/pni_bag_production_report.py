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
            "width": 200
        },
		{
            "fieldname": "nos",
            "label": _("Nos"),
            "fieldtype": "Int",
			"width": 200
        },
		{
            "fieldname": "weight",
            "label": _("Weight"),
            "fieldtype": "Float",
			"width": 200
        }
    ]

def get_data(filters=None):
	conditions = ""
	
	if filters.from_date:
		conditions += " and pb.posting_date >= '{0}' ".format(filters.from_date)
	
	if filters.to_date:
		conditions += " and pb.posting_date <='{0}' ".format(filters.to_date)
	
	if filters.item:
		conditions += " and pb.item = '{0}' ".format(filters.item)
	
	return frappe.db.sql("""
		select 
			pb.item, count(pb.name), sum(pb.weight)
		from
			`tabPNI Bag` as pb
		where
			1=1
			{0}
		group by pb.item
		
	""".format(conditions))