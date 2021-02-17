import frappe


@frappe.whitelist()
def get_items(doctype=None, txt=None, searchfield=None, start=None, page_len=None, filters=None, as_dict=False):
    print(filters)
    doc = frappe.get_doc('Sales Order', filters.get("sales_invoice"))
    items = []
    for item in doc.get('items'):
        items.append(item.item_code)
    return items
