# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns()
	return columns, data

def get_columns():
    return  [
        {
            "fieldname": "employee",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150
        },
		{
            "fieldname": "shift",
            "label": "Shift",
            "fieldtype": "Link",
			"options": "Shift Type",
            "width": 150
        },
		{
            "fieldname": "shift_type",
            "label": "Shift Type",
            "fieldtype": "Data",
        },
		{
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Data",
        }
    ]

def get_data(filters=None):
	conditions = ""

	if filters.shity_type:
		conditions += " and shift_type.shift_type = '{0}' ".format(filters.shity_type)

	return frappe.db.sql("""
		select 
			emp.name,
			emp.default_shift,
			shift_type.shift_type,
			if(count(al.name) > 0,"P","A") as status
		from 
			`tabShift Type` as shift_type,
			`tabEmployee` as emp
		left join
			`tabAttendance Log` as al
		on
			emp.name = al.employee
			and DATE(al.attendance_time) = DATE(now())
		where 
			emp.default_shift = shift_type.name
			{0}
		group by emp.name;
    """.format(conditions))