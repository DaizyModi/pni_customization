import frappe
from frappe.utils import cstr, flt
from erpnext.manufacturing.doctype.bom.bom import BOM as bm

@frappe.whitelist()
def update_bom_with_new_bom(bom):
	update_list_new_bom(bom)
	update_exploded_items(bom)
	return "BOM has been updated with new one."

@frappe.whitelist()
def update_item_name(bom):
	bom_doc = frappe.get_doc("BOM", bom)
	frappe.db.set_value("BOM", bom, "item_name", frappe.get_value("Item", bom_doc.item, "item_name"))
	frappe.db.set_value("BOM", bom, "description", frappe.get_value("Item", bom_doc.item, "description"))
	for raw in bom_doc.items:
		frappe.db.set_value("BOM Item", raw.name, "item_name", frappe.get_value("Item", raw.item_code, "item_name"))
		frappe.db.set_value("BOM Item", raw.name, "description", frappe.get_value("Item", raw.item_code, "description"))
	for raw in bom_doc.exploded_items:
		frappe.db.set_value("BOM Explosion Item", raw.name, "item_name", frappe.get_value("Item", raw.item_code, "item_name"))
		frappe.db.set_value("BOM Explosion Item", raw.name, "description", frappe.get_value("Item", raw.item_code, "description"))
	frappe.db.commit()
	return "Done"

def validate_bom(bom, method):
	bom_list = []
	for raw in bom.items:
		if raw.item_code in bom_list:
			frappe.throw("{0} Item listed multiple time ".format(raw.item_code))
		else:
			bom_list.append(raw.item_code)
def update_list_new_bom(bom):
	master_bom =  frappe.get_doc("BOM", bom)
	for item in master_bom.items:
		print(item.item_code)
		if item.bom_no:
			update_list_new_bom(item.bom_no)
			# continue
		if is_item_has_bom(item.item_code):
			print(item.item_code)
			bom_to = is_item_has_bom(item.item_code)
			unit_cost = get_new_bom_unit_cost(bom_to)
			print(bom_to,unit_cost,item.name)
			frappe.db.sql("""update `tabBOM Item` set bom_no=%s,
			rate=%s, amount=stock_qty*%s where name = %s and docstatus < 2 and parenttype='BOM'""",
			(bom_to, unit_cost, unit_cost, item.name))


def get_new_bom_unit_cost(bom):
	new_bom_unitcost = frappe.db.sql("""SELECT `total_cost`/`quantity`
		FROM `tabBOM` WHERE name = %s""", bom)

	return flt(new_bom_unitcost[0][0]) if new_bom_unitcost else 0
def is_item_has_bom(item):
	bom = frappe.get_all('BOM', 
		filters={
			'item': item, 
			'docstatus': True, 
			'is_active': True, 
			'is_default': True
		}, 
		fields=['name']
	)
	if bom and bom[0]:
		return bom[0].name
	else:
		return None

# def get_exploded_items(bom):
# 	exploded_items = frappe.db.get("BOM Explosion Item", filters={
# 		'parent': bom
# 		}
# 	)
# 	return exploded_items

def update_exploded_items(bom):
	master_bom =  frappe.get_doc("BOM", bom)
	for item in master_bom.items:
		bom_to = is_item_has_bom(item.item_code)
		print(bom_to)
	exploded_items = frappe.db.get("BOM Explosion Item", filters={
		'parent': bom_to
		}
	)

	for items in master_bom.exploded_items:
		print(exploded_items)
		if exploded_items != None:
			frappe.db.sql("""update `tabBOM Explosion Item` set item_code=%s,
				item_name=%s, description=%s, stock_qty=%s, qty_consumed_per_unit=%s, rate=%s, amount=%s where name = %s and docstatus < 2 and parenttype='BOM'""",
				(exploded_items.item_code, exploded_items.item_name, exploded_items.description, exploded_items.stock_qty , exploded_items.qty_consumed_per_unit, exploded_items.rate, exploded_items.amount, items.name))
		else:
			return "BOM has no Exploded Items."

@frappe.whitelist()
def update_bom_default_active(bom):
	list_for_bom = {}	
	update_list_bom(bom, list_for_bom)
	frappe.enqueue("pni_customization.utility.bom_utility.enqueue_bom_processing", _args=list_for_bom, timeout=90000)
	return list_for_bom

def enqueue_bom_processing(_args):
	frappe.db.auto_commit_on_many_writes = 1
	for args in _args:
		doc = frappe.get_doc("BOM Update Tool")
		doc.current_bom = args
		doc.new_bom = _args[args]
		doc.replace_bom()
	frappe.db.auto_commit_on_many_writes = 0
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
	frappe.msgprint(str(args))
	frappe.enqueue("erpnext.manufacturing.doctype.bom_update_tool.bom_update_tool.replace_bom", args=args, timeout=40000)

@frappe.whitelist()
def include_item_in_manufacturing(bom):
	bom = frappe.get_doc("BOM", bom)
	for item in bom.items:
		frappe.db.set_value("BOM Item", item.name, "include_item_in_manufacturing", True)
	return "Success"

@frappe.whitelist()
def get_items(name):
	items = frappe.get_all('Items', filters={'parent':name}, fields=['item_code','item_name'])
	print(items)
	return items
