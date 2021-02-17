import frappe


@frappe.whitelist()
def get_items(filters):
    print(filters)
    doc = frappe.get_doc('Sales Order', filters.get("sales_invoice"))
    for item in doc.get('items'):
        return item.item_code
