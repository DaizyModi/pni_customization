import frappe

@frappe.whitelist()
def get_stock_entry_data(stock_entry):
	return  frappe.get_list("Stock Entry Detail", 
		fields=["s_warehouse","t_warehouse","item_code","item_group","qty"],
		filters={ "docstatus":1, "parent":stock_entry}
	)

def validate_purchase_order(po):
	for raw in po.items:
		try:
			sup = frappe.get_doc("Item Supplier", {"parent": raw.item_code,"supplier":po.supplier})
		except:
			frappe.throw("Item {0} is not configured with {1} supplier".format(raw.item_code,po.supplier))