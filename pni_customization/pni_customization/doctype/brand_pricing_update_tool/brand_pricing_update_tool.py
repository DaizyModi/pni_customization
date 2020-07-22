# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BrandPricingUpdateTool(Document):
	def get_brand_list(self):
		if self.brand_group:
			doc = frappe.get_doc("Brand Group", self.brand_group)
			if doc:
				return doc.brand_group_table
	
	def get_brand_rate(self):
		data = {}
		for row in self.brand_pricing_table:
			value = frappe.db.get_value("Item Price",{"brand":row.brand, "selling": True} ,"price_list_rate" )
			data[row.brand] = value
		return data
	
	def validate(self):
		for row in self.brand_pricing_table:
			data = frappe.db.get_list("Item Price", {"brand": row.brand, "selling": True})
			for item_price in data:
				ip = frappe.get_doc("Item Price",item_price.name)
				ip.price_list_rate = row.selling_rate
				ip.save()
