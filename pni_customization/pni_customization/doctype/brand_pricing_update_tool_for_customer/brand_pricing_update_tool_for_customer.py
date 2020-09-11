# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BrandPricingUpdateToolForCustomer(Document):
	def validate(self):
		items = frappe.get_all("Item", 
			filters={
				'brand': self.brand,
				'has_variants': False
			}, 
			fields=['name']
		)
		for item in items:
			item_price = frappe.get_all("Item Price", 
				filters={
					'item_code': item.name,
					'price_list': 'Standard Selling',
					'brand': self.brand,
					'selling': True,
					'customer': self.customer
				},
				fields=['name']
			)
			if len(item_price) > 0:
				#update this
				frappe.db.set_value("Item Price", item_price[0], "price_list_rate", self.selling_rate)
			else:
				#create new one	
				ip = frappe.get_doc({
					"doctype": "Item Price",
					'item_code': item.name,
					'price_list': 'Standard Selling',
					'brand': self.brand,
					'selling': True,
					'customer': self.customer,
					'price_list_rate': self.selling_rate
				})
				ip.insert()
		self.customer = ""
		self.selling_rate = ""
		self.brand = ""
