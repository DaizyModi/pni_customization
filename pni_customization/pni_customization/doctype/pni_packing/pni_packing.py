# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document



class PNIPacking(Document):
	def validate(self):
		total = 0
		for row in self.items:
			total += int(row.total)
		if self.total:
			total += int(self.total)
		self.total_stock = total

		self.create_carton()

		self.update_weight()

		self.update_packing()
	
	def update_packing(self):
		count = {}
		for data in self.carton_data:
			if data.pni_packing_type in count:
				count[data.pni_packing_type] = 1 + count[data.pni_packing_type]
			else:
				count[data.pni_packing_type] = 1
		for row in count:
			self.append("items",{
				"packing": row,
				"nos": count[row]
			})
	def update_weight(self):
		gross_weight = 0
		net_weight = 0
		for row in self.carton_data:
			gross_weight += row.weight if row.weight else 0
			net_weight += row.net_weight if row.net_weight else 0
		self.total_gross_weight = gross_weight
		self.total_net_weight = net_weight
	
	def onload(self):
		setting = frappe.get_doc("PNI Settings","PNI Settings")
		if not self.carton_weight:
			self.carton_weight = setting.paper_cup_carton_weight
	
	def create_carton(self):
		setting = frappe.get_doc("PNI Settings","PNI Settings")
		if not self.carton_weight:
			self.carton_weight = setting.paper_cup_carton_weight
		for data in self.carton_data:
			if data.weight:
				data.net_weight = data.weight - self.carton_weight
			if not data.carton_id:
				doc = frappe.get_doc({
					"doctype": "PNI Carton",
					"item": self.item,
					"item_name": frappe.get_value("Item", self.item, "item_name"),
					"item_description": frappe.get_value("Item", self.item, "description"),
					"size": self.stack_size,
					"no_of_stack": data.packing_size,
					"total": float(self.stack_size) * float(data.packing_size),
				})
				doc.insert()
				data.carton_id = doc.name
			else:
				doc = frappe.get_doc("PNI Carton",data.carton_id)
				doc.gross_weight = data.weight
				doc.net_weight = data.net_weight
				doc.save()
			
	
	def on_submit(self):
		if not self.items:
			frappe.throw("Packing Detail Can't be blank")
		for data in self.carton_data:
			if not data.weight:
				frappe.throw("Weight Can't be empty")
			doc = frappe.get_doc("PNI Carton",data.carton_id)
			doc.submit()
