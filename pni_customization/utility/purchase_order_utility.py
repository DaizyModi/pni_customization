import frappe

@frappe.whitelist()
def get_stock_entry_data(stock_entry):
	return  frappe.get_list("Stock Entry Detail", 
		fields=["s_warehouse","t_warehouse","item_code","item_group","qty"],
		filters={ "docstatus":1, "parent":stock_entry}
	)