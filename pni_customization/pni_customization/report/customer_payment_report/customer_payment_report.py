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
            "fieldname": "sales_person",
            "label": _("Sales Person"),
            "fieldtype": "Link",
            "width": 150,
			"options":"Sales Person"
        },
		{
            "fieldname": "commitment_amt",
            "label": _("Commitment Ammount"),
            "fieldtype": "Float",
            "width": 150,
			"precision":4
        },
		{
            "fieldname": "payment_ammount",
            "label": _("Payment Receive"),
            "fieldtype": "Float",
            "width": 150,
			"precision":4
        }
    ]

def get_data(filters=None):
	condition = ""

	if filters.from_date:
		condition += " and siv.posting_date >= '{0}' ".format(filters.from_date)
	
	if filters.to_date:
		condition += " and siv.posting_date <='{0}' ".format(filters.to_date)
	
	return frappe.db.sql("""
		select 
			siv.sales_person_name, sum(dpr.commitment_amt), sum(per.allocated_amount)
		from
			`tabSales Invoice` as siv,
			`tabDaily Payment Report` as dpr
		left join
			`tabPayment Entry Reference` as per
		on siv.name = per.reference_name
		where
			siv.docstatus = "1" and
			dpr.parent = siv.name and
			per.reference_doctype = "Sales Invoice"
			{0}
		group by siv.name
		""".format(condition))