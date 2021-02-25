import frappe
from frappe.utils import time_diff_in_hours


def shift_type_validate(doc, method):
    time_diff = time_diff_in_hours(doc.end_time, doc.start_time)
    doc.total_hours = str(time_diff)
