import frappe
from frappe.utils import time_diff_in_hours
from datetime import datetime


def shift_type_validate(doc, method):
    if doc.end_time > doc.start_time:
        time_diff = time_diff_in_hours(doc.end_time, doc.start_time)
        doc.total_hours = time_diff
    else:
        time_start_str = '23:59:59'
        time_start_obj = datetime.strptime(time_start_str, '%H:%M:%S')
        shift_start = time_start_obj.time()
        start_time = time_diff_in_hours(str(shift_start), doc.start_time)

        time_end_str = '00:00:00'
        time_end_obj = datetime.strptime(time_end_str, '%H:%M:%S')
        shift_end = time_end_obj.time()
        end_time = time_diff_in_hours(doc.end_time, str(shift_end))
        time_diff = end_time + start_time

        doc.total_hours = time_diff
