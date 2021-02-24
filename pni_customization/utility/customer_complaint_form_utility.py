import frappe


@frappe.whitelist()
def get_items(doctype=None, txt=None, searchfield=None, start=None, page_len=None, filters=None, as_dict=False):
    print("***********************")
    print(filters)
    doc = frappe.get_doc('Sales Order', filters.get("sales_invoice"))
    items = []
    for item in doc.get('items'):
        items.append({"name": item.item_code, "item_name": "sdafsd",
                      "description": "sdfsd", "item_group": "sdf"})
    print(items)
    return items
    return frappe.db.sql("""select tabItem.name,
		if(length(tabItem.item_name) > 40,
			concat(substr(tabItem.item_name, 1, 40), "..."), item_name) as item_name,
		tabItem.item_group,
		if(length(tabItem.description) > 40, \
			concat(substr(tabItem.description, 1, 40), "..."), description) as description
		{columns}
		from tabItem
		where tabItem.docstatus < 2
			and tabItem.has_variants=0
			and tabItem.disabled=0
			and (tabItem.end_of_life > %(today)s or ifnull(tabItem.end_of_life, '0000-00-00')='0000-00-00')
			and ({scond} or tabItem.item_code IN (select parent from `tabItem Barcode` where barcode LIKE %(txt)s)
				{description_cond})
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, item_name), locate(%(_txt)s, item_name), 99999),
			idx desc,
			name, item_name
		limit %(start)s, %(page_len)s """.format(
        columns=columns,
        scond=searchfields,
        fcond=get_filters_cond(
            doctype, filters, conditions).replace('%', '%%'),
        mcond=get_match_cond(doctype).replace('%', '%%'),
        description_cond=description_cond),
        {
        "today": nowdate(),
        "txt": "%%%s%%" % txt,
        "_txt": txt.replace("%", ""),
        "start": start,
        "page_len": page_len
    }, as_dict=as_dict)


@frappe.whitelist()
def get_invoice_items(sales_invoice):
    doc = frappe.get_doc("Sales Invoice", sales_invoice)
    items = []
    for item in doc.get('items'):
        items.append(item)
    return items
