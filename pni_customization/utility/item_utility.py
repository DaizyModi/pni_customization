import frappe
from erpnext.controllers.item_variant import make_variant_item_code
from frappe.utils import strip

def autoname(doc, method):
	if frappe.db.get_default("item_naming_by") == "Naming Series" and doc.pni_material_type == "Machinery":
		if doc.variant_of:
			if not doc.item_code:
				template_item_name = frappe.db.get_value("Item", doc.variant_of, "item_name")
				doc.item_code = make_variant_item_code(doc.variant_of, template_item_name, doc)
		else:
			from frappe.model.naming import set_name_by_naming_series
			set_name_by_naming_series(doc)
			doc.item_code = doc.name
	else:
		if not doc.pni_item_code and not doc.variant_of:
			frappe.throw("PNI Item Code Mandatory "+doc.item_code)
		if doc.pni_item_code:
			doc.item_code = doc.pni_item_code

	doc.item_code = strip(doc.item_code)
	doc.name = doc.item_code
	frappe.msgprint(doc.item_code)
	frappe.msgprint(doc.name)