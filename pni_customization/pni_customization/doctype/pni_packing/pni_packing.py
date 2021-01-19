# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours


class PNIPacking(Document):
	def validate(self):
		if not self.packing_unit or not self.conversation_factor:
			frappe.throw("Packing Unit and Conversation Factor is mandatory.")
		self.update_employee()
		self.create_carton()

		self.update_weight()

		# self.update_packing()

		self.calculate_total_stock()
		self.set_machine_helper()
		self.first_carton()
	
	def first_carton(self):
		if not self.total_stock:
			self.total_stock = 0
		if not self.loose_stock:
			self.loose_stock = 0
		if not self.last_shift_loose_stock:
			self.last_shift_loose_stock = 0
		self.total_shift_stock = float(self.total_stock) + float(self.loose_stock) - float(self.last_shift_loose_stock)
		if self.pni_packing == self.name:
			frappe.throw("Can't be "+ self.pni_packing)
		if self.shift_first_carton:
			if not self.pni_packing:
				self.pni_packing = self.create_packing()
		if self.pni_packing:
			packing =  frappe.get_doc("PNI Packing",self.pni_packing)
			packing.workstation = self.workstation
			packing.item = self.item
			packing.to_warehouse = self.to_warehouse
			packing.packing_unit = self.packing_unit
			packing.conversation_factor = self.conversation_factor
			packing.save()

	def create_packing(self):
		packing = frappe.get_doc({
			"doctype": "PNI Packing",
			"workstation": self.workstation,
			"item": self.item,
			"to_warehouse": self.to_warehouse,
			"packing_unit": self.packing_unit,
			"conversation_factor": self.conversation_factor
		})
		packing.insert()
		return packing.name
	# def get_last_carton(self):
	# 	'''Returns last carton if exists'''
	# 	last_carton = frappe.get_all('PNI Packing', 'name',{"workstation": self.workstation},order_by='creation desc', limit=2)
	# 	return last_carton and last_carton[1] and last_carton[1]['name']		
	def update_packing(self):
		packing =  frappe.get_doc("PNI Packing", self.pni_packing)
		packing.loose_stock = float(self.last_shift_loose_stock)
		packing.total_shift_stock = float(packing.total_stock) + float(packing.loose_stock) - float(packing.last_shift_loose_stock)
		packing.save()
	def update_can_packing(self):
		packing =  frappe.get_doc("PNI Packing", self.pni_packing)
		packing.loose_stock = 0
		packing.total_shift_stock = float(packing.total_stock) + float(packing.loose_stock) - float(packing.last_shift_loose_stock)
		packing.save()
	def set_machine_helper(self):
		helper = ""
		if self.shift == "Day":
			helper = frappe.get_value("Workstation", self.workstation, "workstation_helper_name")
		else:
			helper = frappe.get_value("Workstation", self.workstation, "workstation_helper_name_night_shift")
		self.machine_helper = helper

	def update_employee(self):
		for row in self.employee:
			if row.duty == "Supervisor":
				self.supervisor = row.employee

	def calculate_total_stock(self):
		total = 0
		for row in self.carton_data:
			total += float(self.conversation_factor)
		for row in self.pni_loose_stock:
			total +=  float(row.nos)
		self.total_stock = total
	
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
					"item": self.item,
					"posting_date": self.date	
				})
				doc.insert()
				data.carton_id = doc.name
			if data.carton_id:
				doc2 = frappe.get_doc("PNI Carton",data.carton_id)
				doc2.is_paper_plate = True if self.is_paper_plate else False
				doc2.posting_date = self.date
				doc2.item = self.item
				doc2.shift = self.shift
				doc2.supervisor = self.supervisor
				doc2.supervisor_name =  self.supervisor_name
				doc2.item_name = frappe.get_value("Item", self.item, "item_name")
				doc2.item_description = frappe.get_value("Item", self.item, "description")
				doc2.gross_weight = data.weight
				doc2.net_weight = data.net_weight
				doc2.total = float(self.conversation_factor)
				doc2.warehouse = self.to_warehouse
				doc2.save()
			
	
	def on_submit(self):
		if self.pni_packing:
			self.update_packing()
		if not self.employee:
			frappe.throw("Employee Detail Can't be blank")
		for data in self.carton_data:
			if not data.weight:
				frappe.throw("Weight Can't be empty")
			doc = frappe.get_doc("PNI Carton",data.carton_id)
			doc.submit()
		frappe.db.set(self, 'status', 'Pending For Stock Entry')
	
	def on_cancel(self):
		stock_entry = frappe.db.sql("""select name from `tabStock Entry`
			where pni_reference = %s and docstatus = 1""", self.name)
		if stock_entry:
			frappe.throw("Cannot cancel because submitted Stock Entry \
			{0} exists".format(stock_entry[0][0]))
		frappe.db.set(self, 'status', 'Cancelled')

		for data in self.carton_data:
			crt = frappe.db.get_value("PNI Carton", data.carton_id, "name")		
			if crt:
				doc = frappe.get_doc("PNI Carton",data.carton_id)
				doc.cancel()
				doc.delete()
		if self.pni_packing:
			self.update_can_packing()
	
	def get_employee_list(self):
		if self.select_employee_group:
			doc = frappe.get_doc("Duty Employee Group", self.select_employee_group)
			if doc:
				return doc.employee_team_table
	
	def get_conversation_factor(self):
		item = frappe.get_doc("Item",self.item)
		not_exist = True
		conversion_factor = 0
		for uom in item.uoms:
			if uom.uom == item.sales_uom:
				not_exist = False
				conversion_factor = uom.conversion_factor
				
		if not_exist:
			frappe.throw("Uom Conversation Not Found")
		return conversion_factor
	def manufacture_entry(self):
		return self.make_stock_entry()
	
	def make_stock_entry(self):
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.pni_reference_type = "PNI Packing"
		stock_entry.pni_reference = self.name
		stock_entry.work_station_head = self.workstation_head
		stock_entry.pni_shift = self.shift
		stock_entry.machine_helper = self.machine_helper
		stock_entry.workstation_pni = self.workstation
		stock_entry.posting_date = self.date
		stock_entry.set_posting_time = True
		
		stock_entry.stock_entry_type = "Manufacture"
		stock_entry = self.set_se_items_finish(stock_entry)

		return stock_entry.as_dict()

	def set_se_items_finish(self, se):
		#set from and to warehouse

		se.to_warehouse = self.to_warehouse
		se.from_warehouse = self.source_warehouse

		#TODO allow multiple raw material transfer
		raw_material_cost = 0
		operating_cost = 0
		
		#TODO calc raw_material_cost

		#no timesheet entries, calculate operating cost based on workstation hourly rate and process start, end
		hourly_rate = None
		# hourly_rate = frappe.db.get_value("Workstation", self.workstation, "hour_rate")
		if hourly_rate:
			if self.operation_hours > 0:
				hours = self.operation_hours
			else:
				hours = time_diff_in_hours(self.end_dt, self.start_dt)
				frappe.db.set(self, 'operation_hours', hours)
			operating_cost = hours * float(hourly_rate)
		production_cost = raw_material_cost + operating_cost

		#calc total_qty and total_sale_value
		qty_of_total_production = 0
		total_sale_value = 0
		
		qty_of_total_production = float(qty_of_total_production) + float(self.total_stock)
		
		#add carton to stock entry
		cartons = {}
		for row in self.carton_data:
			if row.carton_item:
				count = cartons.get(row.carton_item, 0)
				cartons.update({row.carton_item:(count + 1)})
		for data in cartons:
			se = self.set_se_items(se, data, None, se.from_warehouse, True, qty_of_total_production, total_sale_value, production_cost, raw_material = cartons[data])

		#add paper cup item to stockentry
		se = self.set_se_items(se, self.item, se.to_warehouse, None, True, qty_of_total_production, total_sale_value, production_cost)
		return se
	
	def set_se_items(self, se, item, t_wh , f_wh , calc_basic_rate=False, qty_of_total_production=None, total_sale_value=None, production_cost=None, raw_material = None):
		
		temp_item = {}
		
		class Empty:
			pass  
		
		temp_item = Empty()
		temp_item.item = item
		temp_item.weight = float(self.total_stock)
		if raw_material:
			temp_item.weight = raw_material
		
		expense_account, cost_center = frappe.db.get_values("Company", self.company, \
			["default_expense_account", "cost_center"])[0]
		item_name, stock_uom, description = frappe.db.get_values("Item", temp_item.item, \
			["item_name", "stock_uom", "description"])[0]

		item_expense_account, item_cost_center = frappe.db.get_value("Item Default", {'parent': temp_item.item, 'company': self.company},\
			["expense_account", "buying_cost_center"])

		if not expense_account and not item_expense_account:
			frappe.throw("Please update default Default Cost of Goods Sold Account for company {0}".format(self.company))

		if not cost_center and not item_cost_center:
			frappe.throw("Please update default Cost Center for company {0}".format(self.company))

		se_item = se.append("items")
		se_item.item_code = temp_item.item
		se_item.qty = temp_item.weight
		if raw_material:
			se_item.s_warehouse = f_wh
		else:
			se_item.t_warehouse = t_wh
		se_item.item_name = item_name
		se_item.description = description
		se_item.uom = stock_uom
		se_item.stock_uom = stock_uom

		se_item.expense_account = item_expense_account or expense_account
		se_item.cost_center = item_cost_center or cost_center

		# in stock uom
		se_item.transfer_qty = temp_item.weight
		se_item.conversion_factor = 1.00

		item_details = se.run_method( "get_item_details",args = (frappe._dict(
		{"item_code": temp_item.item, "company": self.company, "uom": stock_uom, 't_warehouse': t_wh})), for_update=True)

		for f in ("uom", "stock_uom", "description", "item_name", "expense_account",
		"cost_center", "conversion_factor"):
			se_item.set(f, item_details.get(f))

		if calc_basic_rate:
			se_item.basic_rate = production_cost/qty_of_total_production
			# if self.costing_method == "Physical Measurement":
			# 	se_item.basic_rate = production_cost/qty_of_total_production
			# elif self.costing_method == "Relative Sales Value":
			# 	sale_value_of_pdt = frappe.db.get_value("Item Price", {"item_code":item_from_reel.item}, "price_list_rate")
			# 	se_item.basic_rate = (float(sale_value_of_pdt) * float(production_cost)) / float(total_sale_value)
		return se
