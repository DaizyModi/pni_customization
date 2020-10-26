import frappe

@frappe.whitelist()
def include_item_in_manufacturing(work_order):
	wo = frappe.get_doc("Work Order", work_order)
	for item in wo.required_items:
		frappe.db.set_value("Work Order Item", item.name, "include_item_in_manufacturing", True)
	return "Success"