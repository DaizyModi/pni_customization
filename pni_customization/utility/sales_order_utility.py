import frappe
from frappe.utils import today

def sales_order_before_submit(so,method):
	so.transaction_date = today()
	if so.delivery_date < today():
		so.delivery_date = today()