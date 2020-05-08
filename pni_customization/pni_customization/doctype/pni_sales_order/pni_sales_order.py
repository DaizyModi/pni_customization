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
		print("hello")
		target.ignore_pricing_rule = 1
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		if source.company_address:
			target.update({'company_address': source.company_address})
		else:
			# set company address
			target.update(get_company_address(target.company))

		if target.company_address:
			target.update(get_fetch_values("Delivery Note", 'company_address', target.company_address))
		
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
				"doctype":"PNI Sales Order Item"
			}
		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)
	
	return doclist