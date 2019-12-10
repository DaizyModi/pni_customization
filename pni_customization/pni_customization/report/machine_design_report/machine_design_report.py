from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
    columns, data = [], []
    if not filters: filters = {}
    columns =  get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    "Return columns based on filters"
    
    columns = [
            {
                "label": _("Name"),
                "fieldname": "name",
                "fieldtype": "Link",
                "options": "Machine Design Department",
                "width": 150
            },
            {
                "label": _("Employee"),
                "fieldname": "employee",
                "fieldtype": "Link",
                "options": "Employee",
                "width": 150
            },
            {
                "label": _("Employee Name"),
                "fieldname": "employee_name",
                "fieldtype": "Data",
                "width": 150
            },
            {
                "label": _("Date"),
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "width": 150
            },
            {
                "label": _("Time Logs(From Time)"),
                "fieldname": "from_time",
                "fieldtype": "Time",
                "width": 150
            },
            {
                "label": _("Time Logs(To Time)"),
                "fieldname": "to_time",
                "fieldtype": "Time",
                "width": 150
            },
            {
                "label": _("Total Time(In Hrs.)"),
                "fieldname": "total_hours",
                "fieldtype": "Data",
                "width": 150
            }
    ]

    return columns



def get_condition(filters):
    condition = ""
    if filters.get("employee"): condition += "  AND employee = %(employee)s"
    if filters.get("from_date"): condition += " AND posting_date >= %(from_date)s"
    if filters.get("to_date"): condition += " AND posting_date <= %(to_date)s"
    
    return condition

def get_data(filters):
    condition = get_condition(filters)
    
    data = frappe.db.sql("""SELECT m.employee, m.employee_name, m.posting_date, m.name
            FROM `tabMachine Design Department` m where docstatus >= 0 %s """%condition, filters, as_dict=True)

    if(data):
        final_data = []
        for d in data:
            child_list = []
            child_table = frappe.db.sql("""SELECT t.from_time, t.to_time FROM `tabMachine Design Time Logs` t
                            WHERE parent = %s """,(d.name), as_dict=True)

            if(child_table):
                final_data.append({"name": d.name, "employee": d.employee, "employee_name": d.employee_name, "posting_date": d.posting_date, "from_time": "", "to_time": "", "total_hours": ""})
                for c in range(0, len(child_table)):
                    FMT = '%H:%M:%S'
                    if(child_table[c].from_time and child_table[c].to_time):
                        total_hours = str(datetime.strptime(str(child_table[c].to_time), FMT) - datetime.strptime(str(child_table[c].from_time), FMT))
                    else:
                            total_hours = ""
                    child_list.append({"name": "", "employee": "", "employee_name": "", "posting_date": "", "from_time": child_table[c].from_time, "to_time": child_table[c].to_time, "total_hours": total_hours[:4]})


            final_data.extend(child_list)

    return final_data
