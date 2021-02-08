# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    data = get_data(filters)
    columns = get_columns(filters)
    return columns, data


def get_columns(filters):
    if filters.date_wise:
        return [
            {
                "fieldname": "workstation_head",
                "label": _("Workstation Head"),
                "fieldtype": "Data",
                "width": 150
            },
            {
                "fieldname": "date",
                "label": _("Date"),
                "fieldtype": "Date",
                "width": 150
            },
            {
                "fieldname": "machine_helper_id",
                "label": _("Machine Helper ID"),
                "fieldtype": "Link",
                "options": "Employee",
                "width": 150
            },
            {
                "fieldname": "machine_helper",
                "label": _("Machine Helper"),
                "fieldtype": "Data",
                "width": 150
            },
            {
                "fieldname": "total_stock",
                "label": _("Total Stock"),
                "fieldtype": "Float",
                "width": 150,
                "precision": 4
            },
            {
                "fieldname": "total_pay",
                "label": _("Total Pay"),
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
    else:
        return [
            {
                "fieldname": "workstation_head",
                "label": _("Workstation Head"),
                "fieldtype": "Data",
                "width": 150
            },
            {
                "fieldname": "machine_helper_id",
                "label": _("Machine Helper ID"),
                "fieldtype": "Link",
                "options": "Employee",
                "width": 150
            },
            {
                "fieldname": "machine_helper",
                "label": _("Machine Helper"),
                "fieldtype": "Data",
                "width": 150
            },
            {
                "fieldname": "total_stock",
                "label": _("Total Stock"),
                "fieldtype": "Float",
                "width": 150,
                "precision": 4
            },
            {
                "fieldname": "total_pay",
                "label": _("Total Pay"),
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
    columns = """workstation_head,
    machine_helper_id,
    machine_helper,
    sum(total_shift_stock),
    sum(total_shift_stock * rate)"""
    group_by = ""
    if filters.from_date:
        conditions += " and date >= '{0}' ".format(filters.from_date)

    if filters.to_date:
        conditions += " and date <='{0}' ".format(filters.to_date)

    if filters.workstation_head:
        conditions += " and workstation_head like '%{0}%' ".format(
            filters.workstation_head)

    if filters.date_wise:
        columns = """workstation_head,
        date
        machine_helper_id,
        machine_helper,
        sum(total_shift_stock),
        sum(total_shift_stock * rate)"""
        group_by = " ,date"
    return frappe.db.sql(""" select {2} from `tabPNI Packing` where docstatus = 1 {0} group by machine_helper {1};""".format(conditions, group_by, columns))


"""
SET SQL_SAFE_UPDATES = 0;
update `tabPNI Packing` as packing, `tabWorkstation` as workstation set packing.rate = workstation.pni_rate where packing.workstation = workstation.name and packing.name <> "" and workstation.name <> "";
SET SQL_SAFE_UPDATES = 1;
"""
