import frappe


@frappe.whitelist()
def get_items(filters):
    doc = frappe.get_doc('Sales Invoice', filters.get("sales_invoice"))
    for item in doc.get('items'):
        return item.item_code
