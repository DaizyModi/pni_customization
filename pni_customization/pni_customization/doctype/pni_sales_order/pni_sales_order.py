# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, nowdate, getdate
from erpnext.selling.doctype.customer.customer import check_credit_limit,get_credit_limit

class PNISalesOrder(Document):
	def validate(self):
		pass
	
	def on_update(self):
		if self.workflow_state == "Sales Approved":
			if get_credit_limit(self.customer,self.company) != 0:
				check_credit_limit(self.customer, self.company)
				self.workflow_state = "Account Approved"
				self.save()
				self.submit()

# @frappe.whitelist()
# def make_sales_order(source_name, target_doc=None):
# 	return _make_sales_order(source_name, target_doc)

# def _make_sales_order(source_name, target_doc=None, ignore_permissions=False):
# 	pni_so = frappe.get_doc("PNI Sales Order", source_name)
# 	customer = frappe.get_doc("Customer", pni_so.customer) 

# 	def set_missing_values(source, target):
# 		if customer:
# 			target.customer = customer.name
# 			target.customer_name = customer.customer_name
# 		# if source.referral_sales_partner:
# 		# 	target.sales_partner=source.referral_sales_partner
# 		# 	target.commission_rate=frappe.get_value('Sales Partner', source.referral_sales_partner, 'commission_rate')
# 		target.ignore_pricing_rule = 1
# 		target.flags.ignore_permissions = ignore_permissions
# 		target.run_method("set_missing_values")
# 		target.run_method("calculate_taxes_and_totals")

# 	def update_item(obj, target, source_parent):
# 		target.stock_qty = flt(obj.qty) * 1 #flt(obj.conversion_factor)
# 		target.delivery_date = source_parent.delivery_date

# 	def update_sales(obj, target, source_parent):
# 		target.sales_person = source_parent.sales_person
# 		target.allocated_percentage = 100
	
# 	doclist = get_mapped_doc("PNI Sales Order", source_name, {
# 			"PNI Sales Order": {
# 				"doctype": "Sales Order",
# 				"validation": {
# 					"docstatus": ["=", 1]
# 				},
# 				"field_map": {
# 					"date" : "transaction_date",
# 					"delivery_date" : "delivery_date",
# 					"sales_person" : "pni_sales_person"
# 				}
# 			},
# 			"PNI Sales Order Item": {
# 				"doctype": "Sales Order Item",
# 				"field_map": {
# 					"parent": "pni_sales_order",
# 					"item": "item_code",
# 					"qty": "qty_in_carton",
# 					# "uom": 
# 					"rate": "rate"

# 				},
# 				"postprocess": update_item
# 			},
# 			"Sales Team": {
# 				"postprocess": update_sales
# 			},
# 			"Sales Taxes and Charges": {
# 				"doctype": "Sales Taxes and Charges",
# 				"add_if_empty": True
# 			},
# 			"Sales Team": {
# 				"doctype": "Sales Team",
# 				"add_if_empty": True
# 			},
# 			"Payment Schedule": {
# 				"doctype": "Payment Schedule",
# 				"add_if_empty": True
# 			}
# 		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

# 	# postprocess: fetch shipping address, set missing values

# 	return doclist

@frappe.whitelist()
def make_pni_sales_order(source_name, target_doc=None, ignore_permissions = False):
	lead = frappe.get_doc("Lead", source_name)
	customer = frappe.db.get_value("Customer", {"lead_name": lead.name})

	def set_missing_values(source, target):
		if customer:
			target.customer = customer
	
	doclist = get_mapped_doc("Lead", source_name, {
			"Lead": {
				"doctype": "PNI Sales Order",
				"field_map": {
					"name" : "lead",
				}
			}
		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)
	
	return doclist

@frappe.whitelist()
def make_pni_sales_order_from_opportunity(source_name, target_doc=None, ignore_permissions = False):
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
				"doctype": "PNI Sales Order",
				"field_map": {
					"party_name" : "lead",
					"name" : "opportunity"
				}
			}
		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)
	
	return doclist

@frappe.whitelist()
def make_pni_sales_order_from_quotation(source_name, target_doc=None, ignore_permissions = False):
	
	doclist = get_mapped_doc("PNI Quotation", source_name, {
			"PNI Quotation": {
				"doctype": "PNI Sales Order",
				"field_map": {
					"lead" : "lead",
					"opportunity" : "opportunity",
					"name": "pni_quotation"
				}
			},
			"PNI Quotation Item": {
				"doctype": "PNI Sales Order Item",
				"field_map": {
					"Item" : "Item",
					"stack_size" : "stack_size",
					"qty": "qty",
					"uom": "uom",
					"rate": "rate"
				}
			}
		}, target_doc, ignore_permissions=ignore_permissions)
	
	return doclist

@frappe.whitelist()
def make_payment_entry(source_name, target_doc=None, ignore_permissions = False):
	pni_so = frappe.get_doc("PNI Sales Order", source_name)

	def set_missing_values(source, target):
		target.party_type = "Customer"
		target.paid_from = frappe.db.get_value("Account",
						{"company": pni_so.company, "account_type": "Receivable", "is_group": 0})
		# target.run_method("set_missing_values")
	
	doclist = get_mapped_doc("PNI Sales Order", source_name, {
			"PNI Sales Order": {
				"doctype": "Payment Entry",
				"field_map": {
					"name" : "pni_sales_order",
					"customer": "party",
				}
			}
		}, target_doc, ignore_permissions=ignore_permissions)
	
	return doclist

@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None, ignore_permissions = False):
	pni_so = frappe.get_doc("PNI Sales Order", source_name)
	customer = pni_so.customer

	def set_missing_values(source, target):
		target.party_type = "Customer"
		target.paid_from = frappe.db.get_value("Account",
						{"company": pni_so.company, "account_type": "Receivable", "is_group": 0})
		# target.run_method("set_missing_values")
	
	doclist = get_mapped_doc("PNI Sales Order", source_name, {
			"PNI Sales Order": {
				"doctype": "Delivery Note",
				"field_map": {
					"name" : "pni_sales_order",
					"customer": "party",
				}
			},
			"PNI Sales Order Item": {
				"doctype": "PNI Delivery Note Item",
				"field_map": {
					"item": "item",
					"stack_size": "stack_size",
					"qty": "qty",
					"uom": "uom",
					"rate": "rate"
				}
			}
		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)
	
	return doclist