import frappe, json
from frappe.model.mapper import get_mapped_doc

def get_permission_query_conditions_for_lead(user):
	if "System Manager" in frappe.get_roles(user):
		return None
	elif "Sales User" in frappe.get_roles(user):
		return """
		(tabLead.owner = '{user}' ) 
		or 
		(tabLead._assign like '%{user}%')
		""".format(user=user)

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
	pass
	# if doc.item_group == "Paper Cup" and doc.variant_of:
	# 	for atr in doc.attributes:
	# 		if atr.attribute == "PC-Packing":
	# 			frappe.db.set_value("Item", doc.name, "stack_size", str(atr.attribute_value))
	# 			frappe.db.commit()

@frappe.whitelist()
def make_pni_quotation(source_name, target_doc=None, ignore_permissions = False):
	lead = frappe.get_doc("Lead", source_name)
	customer = frappe.db.get_value("Customer", {"lead_name": lead.name})

	def set_missing_values(source, target):
		if customer:
			target.customer = customer
	
	doclist = get_mapped_doc("Lead", source_name, {
			"Lead": {
				"doctype": "PNI Quotation",
				"field_map": {
					"name" : "lead",
				}
			}
		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)
	
	return doclist

@frappe.whitelist()
def make_pni_quotation_from_opportunity(source_name, target_doc=None, ignore_permissions = False):
	opportunity = frappe.get_doc("Opportunity", source_name)
	lead = frappe.get_doc("Lead", opportunity.party_name)
	customer = frappe.db.get_value("Customer", {"lead_name": lead.name})
	if not customer:
		frappe.throw("Please Create Customer first from Lead")
	def set_missing_values(source, target):
		if customer:
			target.customer = customer
	
	doclist = get_mapped_doc("Opportunity", source_name, {
			"Opportunity": {
				"doctype": "PNI Quotation",
				"field_map": {
					"party_name" : "lead",
					"name": "opportunity"
				}
			}
		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)
	
	return doclist


@frappe.whitelist()
def update_delivery_item(doc, method):
	pass
	# if doc.pni_sales_order:
	# 	rate_card = {}
	# 	list_item = {}
	# 	for data in doc.pni_delivery_note:
	# 		rate_card[data.item] = data.rate
	# 	for data in doc.pni_packing_table:
	# 		if not list_item[data.item]:
	# 			list_item[data.item] = 0
	# 		list_item[data.item] += data.total_qty

@frappe.whitelist()
def submit_work_order_item(doc, method):
	return
	if doc.required_items:
		for row in doc.required_items:
			if type(row.available_qty_at_source_warehouse) == "NoneType" or float(row.required_qty) > float(row.available_qty_at_source_warehouse):
				frappe.throw("Work Order Can't be submit as qty is not avaialble at source warehouse")

@frappe.whitelist()
def validate_work_order_item(doc, method):
	print("1")
	if doc.required_items:
		print("2")
		if doc.bom_no:
			bom = frappe.get_doc("BOM",doc.bom_no)
			for row in doc.required_items:
				print("4")
				for bom_item in bom.items:
					print("5")
					if bom_item.item_code == row.item_code:
						print("6")
						row.pni_qty_per_piece = bom_item.pni_qty_per_piece
						# row.save()

@frappe.whitelist()
def validate_stock_entry_item(doc, method):
	print("1")
	if doc.items:
		print("2")
		if doc.bom_no:
			bom = frappe.get_doc("BOM",doc.bom_no)
			if bom:
				for row in doc.items:
					print("4")
					for bom_item in bom.items:
						print("5")
						if bom_item.item_code == row.item_code:
							print("6")
							row.pni_qty_per_piece = bom_item.pni_qty_per_piece
							# row.save()