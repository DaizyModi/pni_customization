import frappe
from erpnext.accounts.party import get_dashboard_info

def validate(doc, method):
	info = get_dashboard_info("Customer", doc.customer)
	if info[0] and info[0]['billing_this_year'] > 5000000:
		exist = False
		for tax in doc.taxes:
			if tax.account_head == "TCS (Tax Collected at Source) - PNI":
				exist = True
		if not exist:
			frappe.throw("TCS (Tax Collected at Source) - PNI Must be added for customer {0} total anual invoice {1} is more then 50,00,000 INR".format(doc.customer,info[0]['billing_this_year']))
				