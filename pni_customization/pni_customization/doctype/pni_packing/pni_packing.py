# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document



class PNIPacking(Document):
	def validate(self):
		self.update_employee()
		self.create_carton()

		self.update_weight()

		# self.update_packing()

		self.calculate_total_stock()
	
	def update_employee(self):
		for row in self.employee:
			if row.duty == "Supervisor":
				self.supervisor = row.employee

	def calculate_total_stock(self):
		total = 0
		for row in self.carton_data:
			total += float(row.stack_size) * float(row.packing_size)
		for row in self.pni_loose_stock:
			total +=  float(row.nos) * float(row.stack_size)
		self.total_stock = total
	# def update_packing(self):
	# 	count = {}
	# 	for data in self.carton_data:
	# 		if data.pni_packing_type in count:
	# 			count[data.pni_packing_type] = 1 + count[data.pni_packing_type]
	# 		else:
	# 			count[data.pni_packing_type] = 1
	# 	self.items = {}
	# 	for row in count:
	# 		self.append("items",{
	# 			"packing": row,
	# 			"packing_size": float(row) ,
	# 			"nos": count[row],
	# 			"total": float(row) * float(count[row]) * float(self.stack_size)
	# 		})
		
	# 	total = 0
		
	# 	for row in self.items:
	# 		total += int(row.total)
	# 	if self.total:
	# 		total += int(self.total)
	# 	self.total_stock = total
	
	def update_weight(self):
		gross_weight = 0
		net_weight = 0
		for row in self.carton_data:
			gross_weight += row.weight if row.weight else 0
			net_weight += row.net_weight if row.net_weight else 0
		loose_weight = float(self.loose_weight) if self.loose_weight else 0
		self.total_gross_weight = gross_weight + loose_weight
		self.total_net_weight = net_weight + loose_weight
	
	def onload(self):
		pass
		# setting = frappe.get_doc("PNI Settings","PNI Settings")
		# if not self.carton_weight:
		# 	self.carton_weight = setting.paper_cup_carton_weight
	
	def create_carton(self):
		setting = frappe.get_doc("PNI Settings","PNI Settings")
		# if not self.carton_weight:
		# 	self.carton_weight = setting.paper_cup_carton_weight
		for data in self.carton_data:
			if data.weight:
				data.net_weight = data.weight - data.carton_weight
			if not data.carton_id:
				doc = frappe.get_doc({
					"doctype": "PNI Carton",
					"naming_series": setting.paper_plate_carton_series if self.is_paper_plate else setting.paper_cup_carton_series,
					"is_paper_plate": True if self.is_paper_plate else False,
					"item": self.item,
					"supervisor": self.supervisor,
					"supervisor_name": self.supervisor_name,
					"shift": self.shift,
					"item_name": frappe.get_value("Item", self.item, "item_name"),
					"item_description": frappe.get_value("Item", self.item, "description"),
					"size": data.stack_size,
					"no_of_stack": data.packing_size,
					"total": float(data.stack_size) * float(data.packing_size),
				})
				doc.insert()
				data.carton_id = doc.name
				data.print_carton = doc.name
			else:
				doc = frappe.get_doc("PNI Carton",data.carton_id)
				doc.gross_weight = data.weight
				doc.net_weight = data.net_weight
				doc.shift = self.shift
				doc.supervisor = self.supervisor
				doc.supervisor_name =  self.supervisor_name
				doc.save()
				data.print_carton = data.carton_id
			
	
	def on_submit(self):
		if not self.employee:
			frappe.throw("Employee Detail Can't be blank")
		for data in self.carton_data:
			if not data.weight:
				frappe.throw("Weight Can't be empty")
			doc = frappe.get_doc("PNI Carton",data.carton_id)
			doc.submit()
	
	def get_employee_list(self):
		if self.select_employee_group:
			doc = frappe.get_doc("Duty Employee Group", self.select_employee_group)
			if doc:
				return doc.employee_team_table
