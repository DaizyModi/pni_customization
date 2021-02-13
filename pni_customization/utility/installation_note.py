import frappe


@frappe.whitelist()
def get_pre_installation_check_item(pre_installation_check):
    doc = frappe.get_doc("Pre Installation Check", pre_installation_check)
    if doc:
        return doc.pre_installation_check_item
