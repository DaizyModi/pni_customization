import frappe

def employee_validate(doc,method):
	if not doc.skip_restriction and not doc.job_applicant:
		frappe.throw("JOB Applicant is Mandatory")