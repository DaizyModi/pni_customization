# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class ReelTracking(Document):
	def validate(self):
		self.create_update_reel()
	
	def create_update_reel(self):
		for row in self.coating_table:
			if not row.reel_out:
				doc = frappe.get_doc({
					"doctype": "Reel",
					"item": self.item,
					"item_name": frappe.get_value("Item", self.item, "item_name"),
					"item_description": frappe.get_value("Item", self.item, "description"),
					"size": data.stack_size,
					"no_of_stack": data.packing_size,
					"total": float(data.stack_size) * float(data.packing_size),
				})
				doc.insert()
				data.carton_id = doc.name
			else:
				doc = frappe.get_doc("PNI Carton",data.carton_id)
				doc.gross_weight = data.weight
				doc.net_weight = data.net_weight
				doc.save()

