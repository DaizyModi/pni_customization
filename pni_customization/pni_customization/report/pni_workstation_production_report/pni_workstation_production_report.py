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
            "fieldname": "parent_item",
            "label": _("Parent Item"),
            "fieldtype": "Link",
			"options": "Item"
        },
		{
            "fieldname": "workstation_head",
            "label": _("Workstation Head"),
            "fieldtype": "Data",
        },
		{
            "fieldname": "machine_helper",
            "label": _("Machine Helper"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "workstation",
            "label": _("Workstation"),
            "fieldtype": "Link",
            "options": "Workstation",
            "width": 150
        },
		{
            "fieldname": "production",
            "label": _("Total Production"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "bottom_scrap",
            "label": _("Total Bottom Scrap"),
            "fieldtype": "Float",
        },
        {
            "fieldname": "blank_scrap",
            "label": _("Total Blank Scrap"),
            "fieldtype": "Float",
        }
    ]
def get_condition(filters):
	condition1,condition2 = "",""
	if filters.get("from_date"): condition1 += " AND packing.date >= %(from_date)s"
	if filters.get("from_date"): condition2 += " AND stock_entry.posting_date >= %(from_date)s"
	if filters.get("to_date"): condition1 += " AND packing.date <= %(to_date)s"
	if filters.get("to_date"): condition2 += " AND stock_entry.posting_date <= %(to_date)s"
	if filters.get("parent_item"): condition1 += " AND item.variant_of = %(parent_item)s"
	if filters.get("item_group"): condition1 += " AND item.item_group = %(item_group)s"
	if filters.get("workstation"): condition1 += " AND packing.workstation = %(workstation)s"
	if filters.get("shift"): condition1 += " and packing.shift = %(shift)s  "

	if filters.get("workstation_head"): 
		filters["workstation_head"] = frappe.get_value("Employee", filters.get("workstation_head"), "employee_name")
		condition1 += " AND packing.workstation_head = %(workstation_head)s "
	
	if filters.get("machine_helper"): 
		filters["machine_helper"] = frappe.get_value("Employee", filters.get("machine_helper"), "employee_name")
		condition1 += " AND packing.machine_helper = %(machine_helper)s "

	if filters.get("employee"):
		filters["employee"] = frappe.get_value("Employee", filters.get("employee"), "employee_name")
		temp_condition1 = 	" and ( 1=0 "
		temp_condition1 += 	" or packing.workstation_head = %(employee)s  "
		temp_condition1+= 	" or packing.machine_helper = %(employee)s "
		temp_condition1 += 	" or ett.employee_name = %(employee)s "
		temp_condition1 += 	" )"
	
	return condition1,condition2

def get_data(filters=None):
	condition1,condition2 = get_condition(filters)
	# `tabEmployee Team Table` as ett
	return frappe.db.sql("""
		select table1.parent_item, table1.workstation_head, table1.machine_helper, table1.workstation,table1.total_production,table2.total_bottom_scrap, table2.total_blank_scrap
			from 
				
				(select 
					item.variant_of as parent_item,
					packing.workstation_head as workstation_head, 
					packing.machine_helper as machine_helper, 
					packing.workstation as workstation, 
					sum(packing.total_stock) as total_production 
				from 
					`tabPNI Packing` as packing, 
					`tabItem` as item,
					
				where 
					ett.parent = packing.name and
					packing.docstatus = "1" and
					item.name = packing.item 
					%s
				group by packing.workstation, packing.workstation_head, packing.machine_helper, item.variant_of) as table1

				left join 
				
				(select 
					stock_entry.pni_reference as workstation,
					SUM(CASE WHEN item_table.item_code = 'Bottom Paper Scrap' THEN item_table.qty ELSE 0 END) as total_bottom_scrap,
					SUM(CASE WHEN item_table.item_code = 'Blank Paper Scrap' THEN item_table.qty ELSE 0 END) as total_blank_scrap
				from 
					`tabStock Entry Detail` as item_table,
					`tabStock Entry` as stock_entry
				
				where
					item_table.parent = stock_entry.name and
					stock_entry.scrap_entry = "1" and
					stock_entry.pni_reference_type = "Workstation"
					%s
				group by stock_entry.pni_reference) as table2
			
			on table1.workstation = table2.workstation
			
    """%(condition1, condition2), filters)