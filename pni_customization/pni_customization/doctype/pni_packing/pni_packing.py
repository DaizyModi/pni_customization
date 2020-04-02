# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours


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
		frappe.db.set(self, 'status', 'Pending For Stock Entry')
	
	def on_cancel(self):
		stock_entry = frappe.db.sql("""select name from `tabStock Entry`
			where pni_reference = %s and docstatus = 1""", self.name)
		if stock_entry:
			frappe.throw("Cannot cancel because submitted Stock Entry \
			{0} exists".format(stock_entry[0][0]))
		frappe.db.set(self, 'status', 'Cancelled')

		for data in self.carton_data:
			doc = frappe.get_doc("PNI Carton",data.carton_id)
			doc.cancel()
	
	def get_employee_list(self):
		if self.select_employee_group:
			doc = frappe.get_doc("Duty Employee Group", self.select_employee_group)
			if doc:
				return doc.employee_team_table
	
	def manufacture_entry(self):
		return self.make_stock_entry()
	
	def make_stock_entry(self):
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.pni_reference_type = "PNI Packing"
		stock_entry.pni_reference = self.name
		
		stock_entry.stock_entry_type = "Material Receipt"
		stock_entry = self.set_se_items_finish(stock_entry)

		return stock_entry.as_dict()

	def set_se_items_finish(self, se):
		#set from and to warehouse

		se.to_warehouse = self.to_warehouse

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

		#add Stock Entry Items for produced goods and scrap
		
		se = self.set_se_items(se, self.item, se.to_warehouse, True, qty_of_total_production, total_sale_value, production_cost)

		return se
	
	def set_se_items(self, se, item, t_wh, calc_basic_rate=False, qty_of_total_production=None, total_sale_value=None, production_cost=None):
		
		temp_item = {}
		
		class Empty:
			pass  
		
		temp_item = Empty()
		temp_item.item = item
		temp_item.weight = float(self.total_stock)
		
		expense_account, cost_center = frappe.db.get_values("Company", self.company, \
			["default_expense_account", "cost_center"])[0]
		item_name, stock_uom, description = frappe.db.get_values("Item", temp_item.item, \
			["item_name", "stock_uom", "description"])[0]

		item_expense_account, item_cost_center = frappe.db.get_value("Item Default", {'parent': temp_item.item, 'company': self.company},\
			["expense_account", "buying_cost_center"])

		if not expense_account and not item_expense_account:
			frappe.throw(_("Please update default Default Cost of Goods Sold Account for company {0}").format(self.company))

		if not cost_center and not item_cost_center:
			frappe.throw(_("Please update default Cost Center for company {0}").format(self.company))

		se_item = se.append("items")
		se_item.item_code = temp_item.item
		se_item.qty = temp_item.weight
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
