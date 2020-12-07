import frappe
from frappe.model.mapper import get_mapped_doc

def job_offer_validate(doc,method):
	if not doc.skip_restriction and not doc.job_applicant:
		frappe.throw("JOB Applicant is Mandatory")

@frappe.whitelist()
def open_employee_onboarding(source_name, target_doc=None, ignore_permissions = False):
	
	doclist = get_mapped_doc("Job Offer", source_name, {
			"Job Offer": {
				"doctype": "Employee Onboarding",
				"field_map": {
					"name" : "job_offer",
					"job_applicant" : "job_applicant"
				}
			}
		}, target_doc)
	
	return doclist