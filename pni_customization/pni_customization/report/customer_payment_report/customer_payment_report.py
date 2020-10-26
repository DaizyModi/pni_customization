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
            "fieldname": "sales_invoice",
            "label": _("Sales Invoice"),
            "fieldtype": "Link",
            "width": 150,
			"options":"Sales Invoice"
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
	condition, condition2 = "",""

	if filters.from_date:
		condition += " and siv.posting_date >= '{0}' ".format(filters.from_date)
		condition2 += " and pe.posting_date >= '{0}' ".format(filters.from_date)
	
	if filters.to_date:
		condition += " and siv.posting_date <='{0}' ".format(filters.to_date)
		condition2 += " and pe.posting_date <='{0}' ".format(filters.to_date)
	
	return frappe.db.sql("""
		select 
			invoice_data.sales_person_name, 
			invoice_data.name, 
			invoice_data.commitment_amt, 
			payment_data.allocated_amount
		from
			(
				select 
					siv.name,
					siv.sales_person_name, 
					sum(dpr.commitment_amt) as commitment_amt
				from
					`tabSales Invoice` as siv
				left join
					`tabDaily Payment Report` as dpr
				on 
					siv.name = dpr.parent
				where
					siv.docstatus = "1"
					{0}
				group by siv.name,siv.sales_person_name
			) as invoice_data
		left join
			(
				select 
					siv.name,
					sum(per.allocated_amount) as allocated_amount
				from
					`tabSales Invoice` as siv
				left join
					`tabPayment Entry Reference` as per
				on 
					siv.name = per.reference_name and per.reference_doctype = "Sales Invoice"
				inner join
					`tabPayment Entry` as pe
				on
					pe.name = per.parent
				where
					siv.docstatus = "1" and 
					per.docstatus = "1"
					{1}
				group by siv.name
			) as payment_data
		on
			invoice_data.name = payment_data.name
		""".format(condition,condition2))