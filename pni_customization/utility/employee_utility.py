import frappe

def employee_validate(doc,method):
	valid,msg = True,"Logs:"
	if not doc.skip_restriction and not doc.job_applicant:
		valid = False
		msg += "JOB Applicant is Mandatory, "
	
	if not doc.skip_restriction and not doc.employee_onboarding:
		valid = False
		msg += "Employee OnBoarding is Mandatory, "
	
	if not is_leave_allocatted(doc) and not doc.skip_restriction:
		if doc.workflow_state == "Pending For Approval":
			valid = False
			msg += "Leave Allocation Pending, "
	
	if not is_shift_allocatted(doc) and not doc.skip_restriction:
		if doc.workflow_state == "Pending For Approval":
			valid = False
			msg += "Shift Allocation Pending, "
	
	if not is_salary_structure_allocatted(doc) and not doc.skip_restriction:
		if doc.workflow_state == "Pending For Approval":
			valid = False
			msg += "Salary Structure Assignment Pending, "
	
	if not valid:
		frappe.throw(msg)

def is_leave_allocatted(employee):
	la = frappe.get_all("Leave Allocation",filters={"docstatus": 1, "employee": employee.name},
		fields= ['name'])
	if la:
		return True
	else:
		return False

def is_shift_allocatted(employee):
	sa = frappe.get_all("Shift Assignment",filters={"docstatus": 1, "employee": employee.name},
		fields= ['name'])
	if sa:
		return True
	else:
		return False

def is_salary_structure_allocatted(employee):
	sa = frappe.get_all("Salary Structure Assignment",filters={"docstatus": 1, "employee": employee.name},
		fields= ['name'])
	if sa:
		return True
	else:
		return False