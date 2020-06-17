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
            "options": "Workstation",
            "width": 150
        },
		{
            "fieldname": "production",
            "label": _("Total Production"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "scrap",
            "label": _("Total Scrap"),
            "fieldtype": "Float",
        }
    ]

def get_data(filters=None):
	conditions = ""

	if filters.status:
		conditions += " and crt.status = '{0}' ".format(filters.status)

	if filters.item:
		conditions += " and crt.item = '{0}' ".format(filters.item)
	
	if filters.brand:
		conditions += " and item.brand = '{0}' ".format(filters.brand)

	return frappe.db.sql("""
		select table1.workstation,table1.total_production,table2.total_scrap
			from 
				(select 
					packing.workstation as workstation, sum(pni_crt.total) as total_production 
				from 
					`tabPNI Carton` as pni_crt,
					`tabPNI Packing` as packing, 
					`tabPNI Packing Carton` as pni_crt_tbl
					
				where 
					pni_crt.name = pni_crt_tbl.carton_id and
					pni_crt_tbl.parent = packing.name	

				group by packing.workstation) as table1,
				(select 
					stock_entry.pni_reference as workstation,
					sum(item_table.qty) as total_scrap
				from 
					`tabStock Entry Detail` as item_table,
					`tabStock Entry` as stock_entry
				
				where
					item_table.name = stock_entry.parent and
					stock_entry.scrap_entry = "1" and
					stock_entry.pni_reference = "Workstation"
				
				group by stock_entry.pni_reference) as table2
			where table1.workstation = table2.workstation
			{0}
    """.format(conditions))