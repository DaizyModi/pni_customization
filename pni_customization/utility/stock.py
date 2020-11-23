def get_valuation_rate(item_code, company, warehouse=None):
	item = get_item_defaults(item_code, company)
	item_group = get_item_group_defaults(item_code, company)
	brand = get_brand_defaults(item_code, company)
	# item = frappe.get_doc("Item", item_code)
	if item.get("is_stock_item"):
		if not warehouse:
			warehouse = item.get("default_warehouse") or item_group.get("default_warehouse") or brand.get("default_warehouse")

		return frappe.db.get_value("Bin", {"item_code": item_code, "warehouse": warehouse},
			["valuation_rate"], as_dict=True) or {"valuation_rate": 0}

	elif not item.get("is_stock_item"):
		valuation_rate =frappe.db.sql("""select sum(base_net_amount) / sum(qty*conversion_factor)
			from `tabPurchase Invoice Item`
			where item_code = %s and docstatus=1""", item_code)

		if valuation_rate:
			return {"valuation_rate": valuation_rate[0][0] or 0.0}
	else:
		return {"valuation_rate": 0.0}