import frappe

def job_applicant_validate(doc,method):
	if not doc.skip_restriction and not doc.job_title:
		frappe.throw("JOB Openning(Job Title) is Mandatory")