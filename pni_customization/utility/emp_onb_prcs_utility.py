import frappe


def emp_onboarding_validate(doc, method):
    if doc.employee:
        emp_no = doc.employee.split('-', 3)
        print(emp_no[2])
        doc.card_number = emp_no[2].zfill(8)
        emp = frappe.get_doc("Employee", doc.employee)
        emp.card_no = doc.card_number
        emp.save(ignore_permissions=True)
