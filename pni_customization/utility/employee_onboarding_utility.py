import frappe

def employee_onboarding_validate(doc, method):
	if not doc.skip_restriction and not doc.job_offer:
		frappe.throw("JOB Offer is Mandatory")