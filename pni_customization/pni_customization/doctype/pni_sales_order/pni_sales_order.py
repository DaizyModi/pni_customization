# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, nowdate, getdate

class PNISalesOrder(Document):
	pass

@frappe.whitelist()
def make_sales_order(source_name, target_doc=None):
	return _make_sales_order(source_name, target_doc)

def _make_sales_order(source_name, target_doc=None, ignore_permissions=False):
	pni_so = frappe.get_doc("PNI Sales Order", source_name)
	customer = frappe.get_doc("Customer", pni_so.customer) 

	def set_missing_values(source, target):
		if customer:
			target.customer = customer.name
			target.customer_name = customer.customer_name
		# if source.referral_sales_partner:
		# 	target.sales_partner=source.referral_sales_partner
		# 	target.commission_rate=frappe.get_value('Sales Partner', source.referral_sales_partner, 'commission_rate')
		target.ignore_pricing_rule = 1
		target.flags.ignore_permissions = ignore_permissions
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item(obj, target, source_parent):
		target.stock_qty = flt(obj.qty) * 1 #flt(obj.conversion_factor)

	doclist = get_mapped_doc("PNI Sales Order", source_name, {
			"PNI Sales Order": {
				"doctype": "Sales Order",
				"validation": {
					"docstatus": ["=", 1]
				}
			},
			"PNI Sales Order Item": {
				"doctype": "Sales Order Item",
				"field_map": {
					"parent": "pni_sales_order",
					"item": "item_code",
					"qty": "qty_in_carton",
					# "uom": 
					"rate": "rate"

				},
				"postprocess": update_item
			},
			"Sales Taxes and Charges": {
				"doctype": "Sales Taxes and Charges",
				"add_if_empty": True
			},
			"Sales Team": {
				"doctype": "Sales Team",
				"add_if_empty": True
			},
			"Payment Schedule": {
				"doctype": "Payment Schedule",
				"add_if_empty": True
			}
		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

	# postprocess: fetch shipping address, set missing values

	return doclist