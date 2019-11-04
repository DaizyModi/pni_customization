import frappe, json

def get_permission_query_conditions_for_opportunity(user):
    	if "System Manager" in frappe.get_roles(user):
    		return None
    	elif "Sales User" in frappe.get_roles(user):
    		return """
			(tabOpportunity.owner = '{user}' ) 
			or 
			(
				tabOpportunity.name in 
					(
						select tabOpportunity.name 
							from tabOpportunity 
								where 			
									tabOpportunity._assign = '["{user}"]'
					)
			)""".format(user=frappe.db.escape(user))

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
def get_item(values):
	attributes = json.loads(values)
	for attribute in attributes:
		print(attribute)
		print(attributes[attribute])
	items = frappe.get_all("Item",{"variant_of":"Test A"})
	for item in items:
		is_varient = True
		item_doc = frappe.get_doc("Item", item)
		for varient_attribute in item_doc.attributes:
			if unicode(varient_attribute.attribute_value) != unicode(attributes[varient_attribute.attribute]):
				is_varient = False
		if is_varient == True:
			return item_doc.name
	return frappe.throw("Item Not Found")