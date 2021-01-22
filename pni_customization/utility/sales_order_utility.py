import frappe
from frappe.utils import today
from erpnext.selling.doctype.customer.customer import get_customer_outstanding, get_credit_limit

def sales_order_before_submit(so,method):
	so.transaction_date = today()
	if so.delivery_date < today():
		so.delivery_date = today()

@frappe.whitelist()
def get_credit_details(customer, company):
	outstanding = get_customer_outstanding(customer, company)
	credit_limit = get_credit_limit(customer, company)
	bal = credit_limit - outstanding
	return {"outstanding":outstanding, "credit_limit":credit_limit, "bal": bal}
