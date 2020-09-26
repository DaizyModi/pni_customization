import frappe

@frappe.whitelist()
def update_bom_default_active(bom):
	list_for_bom = {}	
	update_list_bom(bom, list_for_bom)
	for _bom in list_for_bom:
		frappe.msgprint(" Bom will Replace {0} with {1} ".format(_bom, list_for_bom[_bom]))
		enque_bom_update(_bom,list_for_bom[_bom])
	return "Success"

def update_list_bom(bom, list_for_bom):
	master_bom =  frappe.get_doc("BOM", bom)
	for item in master_bom.items:
		if item.bom_no:
			update_list_bom(item.bom_no, list_for_bom)
			if  not check_bom_is_active_default(item.bom_no):
				new_bom = get_bom_active_default(item.item_code)
				if new_bom:
					list_for_bom[item.bom_no] = new_bom

def get_bom_active_default(item):
	bom = frappe.get_all('BOM', 
		filters={
			'item': item, 
			'docstatus': True, 
			'is_active': True, 
			'is_default': True
		}, 
		fields=['name']
	)
	if bom[0]:
		return bom[0].name
	else:
		return None

def check_bom_is_active_default(bom):
	"""
		Check if current bom is active and also is default
	"""
	bom_obj = frappe.get_doc("BOM", bom)
	if bom_obj.is_active and bom_obj.is_default:
		return True
	else:
		return False

def enque_bom_update(current_bom, new_bom):
	"""
		Enque Bom Replace Process
	"""
	args = {
		"current_bom": current_bom,
		"new_bom": new_bom
	}
	frappe.enqueue("erpnext.manufacturing.doctype.bom_update_tool.bom_update_tool.replace_bom", args=args, timeout=40000)