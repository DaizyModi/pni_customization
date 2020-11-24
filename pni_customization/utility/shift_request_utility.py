import frappe
from frappe.utils import getdate,today

def validate_shift_request(doc, method):
	if getdate(doc.from_date) < today():
		frappe.throw("From Date can't be back date")