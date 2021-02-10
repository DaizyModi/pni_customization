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
    return [
        {
            "fieldname": "person_type",
            "label": _("Person Type"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "employee",
            "label": _("Employee|Worker"),
            "fieldtype": "Dynamic Link",
            "options": "person_type",
            "width": 150
        },
        {
            "fieldname": "emaployee_name",
            "label": _("Emp|Worker Name"),
            "fieldtype": "Data",
            "width": 150,
            "precision": 4
        },
        {
            "fieldname": "item",
            "label": _("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150,
            "precision": 4
        },
        {
            "fieldname": "packing_category",
            "label": _("Packing Category"),
            "fieldtype": "Link",
            "options": "Packing Category",
            "width": 150,
            "precision": 4
        },
        {
            "fieldname": "bag",
            "label": _("Packing Nos"),
            "fieldtype": "Float",
            "width": 150,
            "precision": 4
        },
        {
            "fieldname": "weight",
            "label": _("Weight"),
            "fieldtype": "Float",
            "width": 150,
            "precision": 4
        },
        {
            "fieldname": "paying_amount",
            "label": _("Billing"),
            "fieldtype": "Float",
            "width": 150,
            "precision": 4
        },
        {
            "fieldname": "dumy",
            "label": _("Empty"),
            "fieldtype": "Data",
            "width": 150,
            "precision": 4
        }
    ]


def get_data(filters=None):
    conditions = ""
    if filters.from_date:
        conditions += " and packing.date >= '{0}' ".format(filters.from_date)

    if filters.to_date:
        conditions += " and packing.date <='{0}' ".format(filters.to_date)

    # if filters.workstation_head:
    # 	conditions += " and workstation_head like '%{0}%' ".format(filters.workstation_head)

    return frappe.db.sql("""
		select 
			packing_table.person_type,
			packing_table.employee,
			packing_table.emaployee_name,
			packing_table.item,
			packing_table.packing_category,
			sum(packing_table.bag),
			sum(packing_table.bag * packing_table.bag_size) as weight,
			sum(packing_table.paying_amount)
		from
			`tabPacking Table` as packing_table, `tabPacking` as packing
		where
			packing.docstatus = 1 and packing.name = packing_table.parent {0}
		group by 
			packing_table.employee,packing_table.packing_category,packing_table.item;
    """.format(conditions))


"""
SET SQL_SAFE_UPDATES = 0;
update `tabPNI Packing` as packing, `tabWorkstation` as workstation set packing.rate = workstation.pni_rate where packing.workstation = workstation.name and packing.name <> "" and workstation.name <> "";
SET SQL_SAFE_UPDATES = 1;
"""
