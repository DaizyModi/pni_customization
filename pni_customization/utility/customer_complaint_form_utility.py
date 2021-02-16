import frappe

@frappe.whitelist()
def get_items(sales_invoice):
    doc = frappe.get_doc('Sales Invoice', sales_invoice)
    for item in doc.get('items'):
        return item.item_code