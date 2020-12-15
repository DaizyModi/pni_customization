import frappe

def employee_onboarding_validate(doc, method):
	if not doc.skip_restriction and not doc.job_application:
		frappe.throw("JOB Application is Mandatory")