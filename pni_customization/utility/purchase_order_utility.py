import frappe

@frappe.whitelist()
def get_stock_entry_data(stock_entry):
	return  frappe.get_list("Stock Entry Detail", 
		fields=["s_warehouse","t_warehouse","item_code","item_group","qty"],
		filters={ "docstatus":1, "parent":stock_entry}
	)

def validate_purchase_order(po):
	if not po.skip_supplier_item_validation:
		for raw in po.items:
			try:
				sup = frappe.get_doc("Item Supplier", {"parent": raw.item_code,"supplier":po.supplier})
			except:
				frappe.throw("Item {0} is not configured with {1} supplier".format(raw.item_code,po.supplier))
	restricted_value = ["Cartage - PNI","Courier Charges - PNI","Freight and Forwarding Charges - PNI","Insurance Charges - PNI","Packing Charges - PNI"]
	for raw in po.taxes:
		if raw.account_head in restricted_value and raw.tax_amount > 0:
			po.extra_charges = True


def update_item():
	pos = frappe.get_all("Purchase Order",{"docstatus": [ "in", ["1","0"]]})
	frappe.db.commit()
	for po in pos:
		po_doc = frappe.get_doc("Purchase Order",po.name)
		frappe.db.commit()
		for item in po_doc.items:
			item_po_details = frappe.get_value("Item Supplier",{"parent": item.item_code,"supplier":po_doc.supplier},"name")
			frappe.db.commit()
			if not item_po_details:
				item_doc = frappe.get_doc("Item",item.item_code)
				item_doc.append("supplier_items",{"supplier":po_doc.supplier})
				item_doc.save()
				frappe.db.commit()