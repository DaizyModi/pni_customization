import frappe, json

def get_permission_query_conditions_for_opportunity(user):
	if "System Manager" in frappe.get_roles(user):
		return None
	elif "Sales User" in frappe.get_roles(user):
		return """
		(tabOpportunity.owner = '{user}' ) 
		or 
		(tabOpportunity._assign like '%{user}%')
		""".format(user=user)

@frappe.whitelist()
def get_item_data(item):
	#return item data
	item_doc = frappe.get_doc("Item", item)
	attribute_data = {}
	for row in item_doc.attributes:
		attribute_doc = frappe.get_doc("Item Attribute", row.attribute)
		
		values = []
		for attr_value in attribute_doc.item_attribute_values:
			values.append(attr_value.attribute_value)
		
		if not attribute_doc.numeric_values:
			attribute_data.update({row.attribute: {"numeric_values": False, "values": values}})
		else:
			attribute_data.update({row.attribute: {"numeric_values": True, "values": []}})
		
	return { 
		"item":item, 
		"attribute_data":attribute_data
	}

@frappe.whitelist()
def get_item(item, values):
	attributes = json.loads(values)
	items = frappe.get_all("Item",{"variant_of":item})
	for item in items:
		is_varient = True
		item_doc = frappe.get_doc("Item", item)
		for varient_attribute in item_doc.attributes:
			if str(varient_attribute.attribute_value) != str(attributes[varient_attribute.attribute]):
				is_varient = False
		if is_varient == True:
			return item_doc
	return frappe.throw("Item Not Found")

@frappe.whitelist()
def update_item(doc, method):
	if doc.item_group == "Paper Cup" and doc.variant_of:
		for atr in doc.attributes:
			if atr.attribute == "PC-Packing":
				frappe.db.set_value("Item", doc.name, "stack_size", str(atr.attribute_value))
				frappe.db.commit()