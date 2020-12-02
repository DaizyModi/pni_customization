import frappe

@frappe.whitelist()
def include_item_in_manufacturing(work_order):
	wo = frappe.get_doc("Work Order", work_order)
	for item in wo.required_items:
		frappe.db.set_value("Work Order Item", item.name, "include_item_in_manufacturing", True)
	return "Success"

@frappe.whitelist()
def short_closed(work_order):
	frappe.db.set_value("Work Order", work_order, "short_closed", True)
	return "Success"

@frappe.whitelist()
def short_closed_after_complete(work_order):	
	frappe.db.set_value("Work Order", work_order, "short_closed", True)
	return "Success"