import frappe, json
from frappe.model.mapper import get_mapped_doc
from frappe import _

def validate_reel_qty(doc):
	for item in doc.items:
		if item.is_reel_item:
			if not doc.reel_table_purchase:
				frappe.throw("Reel Entry needed for Item "+item.item_code)
			if not item.reel_brand:
				frappe.throw("Reel Brand is Mandatory for Item " + item.item_code)
			reel_weight = 0
			for reel in doc.reel_table_purchase:
				if (reel.item == item.item_code and 
					item.reel_brand == reel.brand):
					reel_weight += reel.weight
			if reel_weight < item.qty:
				frappe.throw("Total Reel Qty for item  {0} is less then {1} ".format(item.item_code, item.qty))

def validate_reel(doc, method):
	total_weight = 0
	for reel in doc.reel_table_purchase:
		total_weight += reel.weight
	doc.total_reel_weight = total_weight

def create_reel(doc, method):
	validate_reel_qty(doc)
	if doc.reel_item:
		for item in doc.reel_table_purchase:
			doc = frappe.get_doc({
				"doctype": "Reel",
				"status": "In Stock",
				"reel_id": item.reel_id,
				"supplier_reel_id": item.reel_id,
				"warehouse": item.accepted_warehouse,
				"item": item.item,
				"type": "Blank Reel",
				"blank_weight": item.weight,
				"brand": item.brand,
				"weight": item.weight
			})
			doc.insert(ignore_permissions=True)
			doc.submit()

def cancel_reel(doc, method):
	if doc.reel_item:
		for item in doc.reel_table_purchase:
			reel_out = frappe.get_doc("Reel",item.reel_id)
			reel_out.cancel()
			reel_out.delete()

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
def get_carton(carton, items):
	carton = frappe.get_doc("PNI Carton",carton)
	if carton.item not in items.split(",") and items != "":
		frappe.throw("Carton Item not match with PNI Delivery Note Item")
	if carton and carton.status == "Available":
		return carton
	else:
		frappe.throw("Carton Not Available with "+carton.name)

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
def submit_delivery_item(doc, method):
	for row in doc.pni_packing_table:
		carton = frappe.get_doc("PNI Carton", row.pni_carton)
		carton.status = "Delivered"
		carton.save()

@frappe.whitelist()
def cancel_delivery_item(doc, method):
	for row in doc.pni_packing_table:
		carton = frappe.get_doc("PNI Carton", row.pni_carton)
		carton.status = "Available"
		carton.save()

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
	pass

@frappe.whitelist()
def validate_inspection_for_work_order(doc, method):
	print("hello")
	if doc.work_order and doc.stock_entry_type == "Manufacture":
		wo = frappe.get_doc("Work Order", doc.work_order)
		if wo:
			total_qty = wo.qty
			pni_qi = frappe.get_all("PNI Quality Inspection",{"reference_name":wo.name, "docstatus": 1})
			inspect_qty = 0
			for qi in pni_qi:
				pni_qi_doc = frappe.get_doc("PNI Quality Inspection", qi.name)
				inspect_qty += int(pni_qi_doc.accepted_qty)
			if inspect_qty < total_qty:
				frappe.throw(" Please do PNI Quality Inspection for {0} Items".format(str( total_qty- inspect_qty )))

@frappe.whitelist()
def validate_work_order_item(doc, method):
	if doc.required_items:
		if doc.bom_no:
			bom = frappe.get_doc("BOM",doc.bom_no)
			for row in doc.required_items:
				if not row.pni_qty_per_piece:
					for bom_item in bom.items:
						if bom_item.item_code == row.item_code:
							row.pni_qty_per_piece = bom_item.pni_qty_per_piece

@frappe.whitelist()
def validate_stock_entry_item(doc, method):
	print("Hello World")
	validate_inspection_for_work_order(doc, method)
	if doc.items:
		if doc.bom_no:
			bom = frappe.get_doc("BOM",doc.bom_no)
			if bom:
				for row in doc.items:
					if not row.pni_qty_per_piece:
						for bom_item in bom.items:
							if bom_item.item_code == row.item_code:
								row.pni_qty_per_piece = bom_item.pni_qty_per_piece

@frappe.whitelist()
def job_card_submit(doc, method):
	total_qty = 0
	for item in doc.time_logs:
		total_qty += item.completed_qty
	pni_qi = frappe.get_all("PNI Quality Inspection",{"reference_name":doc.name, "pre_pni_inspection": False, "docstatus": 1})
	inspect_qty = 0
	for qi in pni_qi:
		pni_qi_doc = frappe.get_doc("PNI Quality Inspection", qi.name)
		inspect_qty += int(pni_qi_doc.accepted_qty)
	if inspect_qty < total_qty:
		frappe.throw(" Please do PNI QUality Inspection for {0} Items".format(str( total_qty- inspect_qty )))

@frappe.whitelist()
def job_card_update(doc, method):
	operation = frappe.get_doc("Operation", doc.operation)
	if operation and operation.pre_pni_inspection and doc.job_started:
		total_qty = 0
		for item in doc.time_logs:
			total_qty += item.completed_qty
		pni_qi = frappe.get_all("PNI Quality Inspection",{"reference_name":doc.name, "pre_pni_inspection": True, "docstatus": 1})
		print(total_qty)
		inspect_qty = 0
		for qi in pni_qi:
			pni_qi_doc = frappe.get_doc("PNI Quality Inspection", qi.name)
			inspect_qty += int(pni_qi_doc.accepted_qty)
		if inspect_qty == 0:
			frappe.throw(" Pre PNI Quality Inpection Needed")
		if inspect_qty < total_qty:
			frappe.throw(" Please do Pre PNI QUality Inspection for {0} Items".format(str( total_qty- inspect_qty )))

@frappe.whitelist()
def job_card_onload(doc, method):
	data = frappe.db.sql("""select sum(jctl.completed_qty) from `tabJob Card Time Log` jctl
			INNER JOIN
				`tabJob Card` jc
			on jc.name = jctl.parent
			where jc.work_order = %s and jc.operation = %s and jc.docstatus <> 2""", (doc.work_order, doc.operation))
	if data and data[0] and data[0][0]:
		wo = frappe.get_doc("Work Order",doc.work_order)
		doc.pni_balance_qty = int(wo.qty) - int(data[0][0])
	# doc.save()

def validate_opportunity(doc, method):
	if doc.status == "Closed" or doc.status == "Lost":
		if not doc.pni_attachment:
			frappe.throw("Close or Lost Opportunity  must have PNI Attachments!")

def validate_items(se_items, co_items):
	#validate for items not in coating item
	for se_item in se_items:
		if not filter(lambda x: x == se_item.item_code, co_items):
			frappe.throw(_("Item {0} - {1} cannot be part of this Stock Entry").format(se_item.item_code, se_item.item_name))

def validate_se_qty_coating(se, co):
	validate_material_qty_coating(se.items, co.coating_table)
	validate_ldpe_qty_coating(se.items, co.ldpe_bag)
	validate_scrap_qty_coating(se.items, co.coating_scrap)

def validate_ldpe_qty_coating(se_items, co_items):
	#TODO allow multiple raw material transfer?
	for material in co_items:
		qty = 0
		for item in se_items:
			if(material.reel_in == item.item_code):
				qty += item.qty
		if(qty != material.weight):
			frappe.throw(_("Total quantity of Item {0} - {1} should be {2}"\
			).format(material.item, material.item, material.quantity))

def validate_material_qty_coating(se_items, co_items):
	#TODO allow multiple raw material transfer?
	for material in co_items:
		qty = 0
		for item in se_items:
			if(material.item == item.item_code):
				qty += item.qty
		if(qty != material.quantity):
			frappe.throw(_("Total quantity of Item {0} - {1} should be {2}"\
			).format(material.item, material.item, material.quantity))

def validate_scrap_qty_coating(se_items, co_items):
	#TODO allow multiple raw material transfer?
	for material in co_items:
		qty = 0
		for item in se_items:
			if(material.item == item.item_code):
				qty += item.qty
		if(qty != material.quantity):
			frappe.throw(_("Total quantity of Item {0} - {1} should be {2}"\
			).format(material.item, material.item, material.quantity))

def manage_se_submit(se, co):
	if co.docstatus == 0:
		frappe.throw(_("Submit the  {0} {1} to make Stock Entries").format(co.doctype, co.name))
	
	if co.status in ["Completed", "Cancelled"]:
		frappe.throw("You cannot make entries against Completed/Cancelled Process Orders")
	co.status = "Completed"
	co.flags.ignore_validate_update_after_submit = True
	co.save()

def manage_se_cancel(se, co):
	if(co.status == "Completed"):
		try:
			# validate_material_qty_coating(se.items, co.coating_table)
			co.status = "Pending For Stock Entry"
		except:
			frappe.throw("Please cancel the production stock entry first.")
	else:
		frappe.throw("Process order status must be Completed")
	co.flags.ignore_validate_update_after_submit = True
	co.save()

def validate_po(doc, method):
	for item in doc.items:
		if item.material_request:
			mr = frappe.get_doc("Material Request", item.material_request)
			for mr_item in mr.items:
				if mr_item.item_code == item.item_code:
					if item.qty > mr_item.qty:
						frappe.throw("Purchase Order Qty should not greater then Material Request")

@frappe.whitelist()
def manage_se_changes(doc, method):
	
	if doc.pni_reference and doc.pni_reference_type == "PNI Packing":
		co = frappe.get_doc("PNI Packing", doc.pni_reference)
		if(method=="on_submit"):
			
			co_items = []
			co_items.append(co.item)

			validate_items(doc.items, co_items)
			
			manage_se_submit(doc, co)
		elif(method=="on_cancel"):
			manage_se_cancel(doc, co)
	
	if doc.pni_reference and doc.pni_reference_type == "Coating":
		co = frappe.get_doc("Coating", doc.pni_reference)
		if(method=="on_submit"):
			
			co_items = []
			for item in co.coating_table:
				reel_in = frappe.get_doc("Reel",item.reel_in)
				reel_out = frappe.get_doc("Reel",item.reel_out)
				co_items.append(reel_in.item)
				co_items.append(reel_out.item)
			for item in co.coating_scrap:
				co_items.append(item.item)
			if co.ldpe_bag >0:
				paper_blank_setting = frappe.get_doc("Paper Blank Settings","Paper Blank Settings")
				co_items.append(paper_blank_setting.ldpe_bag)

			validate_items(doc.items, co_items)
			
			# validate_se_qty_coating(doc, co)
			# frappe.throw("Success")
			manage_se_submit(doc, co)
		elif(method=="on_cancel"):
			manage_se_cancel(doc, co)
	
	if doc.pni_reference and doc.pni_reference_type == "Slitting":
		slitting = frappe.get_doc("Slitting", doc.pni_reference)
		if(method=="on_submit"):
			
			slitting_items = []
			for item in slitting.slitting_table:
				reel_in = frappe.get_doc("Reel",item.reel_in)
				reel_out = frappe.get_doc("Reel",item.reel_out)
				slitting_items.append(reel_in.item)
				slitting_items.append(reel_out.item)
			for item in slitting.slitting_scrap:
				slitting_items.append(item.item)

			validate_items(doc.items, slitting_items)
			
			# validate_se_qty_coating(doc, co)
			# frappe.throw("Success")
			manage_se_submit(doc, slitting)
		elif(method=="on_cancel"):
			manage_se_cancel(doc, slitting)
	
	if doc.pni_reference and doc.pni_reference_type == "Printing":
		printing = frappe.get_doc("Printing", doc.pni_reference)
		if(method=="on_submit"):
			
			printing_items = []
			for item in printing.printing_table:
				reel_in = frappe.get_doc("Reel",item.reel_in)
				reel_out = frappe.get_doc("Reel",item.reel_out)
				printing_items.append(reel_in.item)
				printing_items.append(reel_out.item)
			for item in printing.printing_scrap:
				printing_items.append(item.item)
			for item in printing.printing_inc_table:
				printing_items.append(item.item)

			validate_items(doc.items, printing_items)
			
			# validate_se_qty_coating(doc, co)
			# frappe.throw("Success")
			manage_se_submit(doc, printing)
		elif(method=="on_cancel"):
			manage_se_cancel(doc, printing)

	if doc.pni_reference and doc.pni_reference_type == "Punching":
		punching = frappe.get_doc("Punching", doc.pni_reference)
		if(method=="on_submit"):
			
			punching_items = []
			for item in punching.punching_table:
				reel_in = frappe.get_doc("Reel",item.reel_in)
				punch_table = frappe.get_doc("Punch Table",item.punch_table)
				punching_items.append(reel_in.item)
				punching_items.append(punch_table.item)
			for item in punching.punching_scrap:
				punching_items.append(item.item)

			validate_items(doc.items, punching_items)
			
			# validate_se_qty_coating(doc, co)
			# frappe.throw("Success")
			manage_se_submit(doc, punching)
		elif(method=="on_cancel"):
			manage_se_cancel(doc, punching)
	
	if doc.pni_reference and doc.pni_reference_type == "Packing":
		Packing = frappe.get_doc("Packing", doc.pni_reference)
		if(method=="on_submit"):
			
			packing_items = []
			packing_items.append(Packing.item)
			packing_items.append(Packing.bag_item)
			for item in Packing.packing_scrap:
				packing_items.append(item.item)

			validate_items(doc.items, packing_items)
			
			# validate_se_qty_coating(doc, co)
			# frappe.throw("Success")
			manage_se_submit(doc, Packing)
		elif(method=="on_cancel"):
			manage_se_cancel(doc, Packing)

	if doc.pni_reference and doc.pni_reference_type == "PNI Material Transfer":
		Packing = frappe.get_doc("PNI Material Transfer", doc.pni_reference)
		if(method=="on_submit"):
			
			packing_items = []
			packing_items.append(Packing.item)

			validate_items(doc.items, packing_items)
			
			# validate_se_qty_coating(doc, co)
			# frappe.throw("Success")
			manage_se_submit(doc, Packing)
		elif(method=="on_cancel"):
			manage_se_cancel(doc, Packing)