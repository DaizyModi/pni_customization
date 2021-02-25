import frappe
from frappe.utils import getdate, today


def validate_shift_request(doc, method):
    if getdate(doc.from_date) < getdate(today()) and False:
        frappe.throw("From Date can't be back date")


@frappe.whitelist()
def get_shift_detail(name):
    emp_shift = frappe.get_doc('Employee', name)
    shift_type = []
    for data in emp_shift.get('employee_shift_type'):
        shift_type.append(data)
    return shift_type
