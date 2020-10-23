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
            "fieldname": "workstation",
            "label": _("Workstation"),
            "fieldtype": "Link",
            "width": 150,
			"options":"Workstation"
        },
		{
            "fieldname": "workstation_head",
            "label": _("Workstation Head"),
            "fieldtype": "Data",
            "width": 150,
        },
		{
            "fieldname": "shift",
            "label": _("Shift"),
            "fieldtype": "Data",
            "width": 150,
			"precision":4
        },
		{
            "fieldname": "packing",
            "label": _("PNI Packing"),
            "fieldtype": "Float",
            "width": 150,
			"precision":4
        },
		{
            "fieldname": "total_production",
            "label": _("Total Production"),
            "fieldtype": "Float",
            "width": 150,
			"precision":4
        },
		{
            "fieldname": "total_bottom_scrap",
            "label": _("Total Bottom Scrap"),
            "fieldtype": "Float",
            "width": 150,
			"precision":4
        },
		{
            "fieldname": "total_blank_scrap",
            "label": _("Total Blank Scrap"),
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
	condition1, condition2 = "",""
	if filters.from_date:
		condition1 += " and stock_entry.posting_date >= '{0}' ".format(filters.from_date)
		condition2 += " and packing.date >= '{0}' ".format(filters.from_date)
	
	if filters.to_date:
		condition1 += " and stock_entry.posting_date <='{0}' ".format(filters.to_date)
		condition2 += " and packing.date <='{0}' ".format(filters.to_date)
	
	if filters.workstation_head:
		workstation_head = frappe.get_value("Employee", filters.get("workstation_head"), "employee_name")
		condition1 += " and workstation.workstation_head_name = '{0}' ".format(workstation_head)
		condition2 += " and packing.workstation_head = '{0}' ".format(workstation_head)
	
	if filters.workstation:
		condition1 += " and stock_entry.pni_reference = '{0}' ".format(filters.workstation)
		condition2 += " and packing.workstation ='{0}' ".format(filters.workstation)
	
	if filters.shift:
		condition1 += " and stock_entry.pni_shift = '{0}' ".format(filters.shift)
		condition2 += " and packing.shift ='{0}' ".format(filters.shift)
	
	return frappe.db.sql("""
		select 
			scrap_data.workstation, 
			scrap_data.workstation_head_name, 
			scrap_data.pni_shift, 
			production_data.packing,
			production_data.production,
			scrap_data.total_bottom_scrap, 
			scrap_data.total_blank_scrap
		from
			(
				select 
					stock_entry.pni_reference as workstation,
					workstation.workstation_head_name as workstation_head_name,
					stock_entry.pni_shift,
					SUM(CASE WHEN item_table.item_code = 'Bottom Paper Scrap' THEN item_table.qty ELSE 0 END) as total_bottom_scrap,
					SUM(CASE WHEN item_table.item_code = 'Blank Paper Scrap' THEN item_table.qty ELSE 0 END) as total_blank_scrap
				from 
					`tabStock Entry Detail` as item_table,
					`tabStock Entry` as stock_entry,
					`tabWorkstation` as workstation
				where
					workstation.name = stock_entry.pni_reference and
					item_table.parent = stock_entry.name and
					stock_entry.scrap_entry = "1" and
					stock_entry.docstatus = "1" and
					stock_entry.pni_reference_type = "Workstation"
					{0}
				group by 
					stock_entry.pni_reference, stock_entry.pni_shift
			) as scrap_data
		FULL JOIN
			(
				select
					count(packing.name) as packing,
					packing.shift,
					packing.workstation,
					sum(packing.total_shift_stock) as production
				from
					`tabPNI Packing` as packing
				where
					packing.docstatus = "1"
					{1}
				group by
					packing.shift,packing.workstation
			) as production_data
		on  
			scrap_data.pni_shift = production_data.shift and 
			scrap_data.workstation = production_data.workstation
    """.format(condition1, condition2))