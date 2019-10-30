import frappe

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
	item_doc = frappe.get_doc("Item", item)
	return {"message":"hello world", "item":item, "attribute":item_doc.attributes}