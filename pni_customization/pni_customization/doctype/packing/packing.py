# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours

class Packing(Document):
	def validate(self):
		self.manage_table()
		if self.end_dt and self.start_dt:
			hours = time_diff_in_hours(self.end_dt, self.start_dt)
			frappe.db.set(self, 'operation_hours', hours)

	def onload(self):
		paper_blank_setting = frappe.get_doc("Paper Blank Settings","Paper Blank Settings")
		self.set_onload("scrapitemgroup", paper_blank_setting.packing_scrap)

	def manage_table(self):
		bag  = 0
		total_weight = 0
		for data in self.packing_table:
			if data.bag_size and data.bag:
				bag += int(data.bag)
				total_weight += float(data.bag_size) * float(data.bag)
		self.total_bag = bag
		self.total_weight = total_weight

		self.bag_item = self.item
	
	def manage_reel_tracking(self, bag):
		doc = frappe.get_doc({
			"doctype": "Reel Tracking",
			"status": "Draft",
			"reel": self.punch_table,
			"reel_process": "Packing",
			"date": frappe.utils.nowdate(),
			"time": frappe.utils.nowtime(),
			"out_reel": bag,
			"status": "Packing Submit",
			"process_reference": self.name
		})
		doc.insert(ignore_permissions=True)
	
	def cancel_reel_tracking(self, bag):
		doc = frappe.get_doc({
			"doctype": "Reel Tracking",
			"status": "Draft",
			"reel": self.punch_table,
			"reel_process": "Packing",
			"date": frappe.utils.nowdate(),
			"time": frappe.utils.nowtime(),
			"out_reel": bag,
			"status": "Packing Cancel",
			"process_reference": self.name
		})
		doc.insert(ignore_permissions=True)

	def on_submit(self):
		if (not self.end_dt) or (not self.end_dt):
			frappe.throw("Please Select Operation Start and End Time")
		for item in self.packing_table:
			if not item.employee:
				frappe.throw("Employee is Compulsory")
		if not self.punch_table:
			frappe.throw("Punch Table is Compulsory")

		punch_table = frappe.get_doc("Punch Table",self.punch_table)
		punch_table.status = "Consume"
		punch_table.save()
		
		for row in self.packing_table:
			if row.bag and row.bag_size:
				for numb in range(row.bag):
					doc = frappe.get_doc({
						"doctype": "PNI Bag",
						"status": "In Stock",
						"item": self.item,
						"punching_die": self.punching_die,
						"packing_category": row.packing_category,
						"supplier_reel_id": punch_table.supplier_reel_id,
						"brand": self.brand,
						"coated_reel": self.coated_reel,
						"printed_reel": self.printed_reel,
						"weight": row.bag_size,
						"reference": self.name,
						"warehouse": self.fg_warehouse,
						"reference_doc": "Packing"
					})
					doc.insert()
					doc.submit()
					self.manage_reel_tracking(doc.name)
		frappe.db.set(self, 'status', 'Pending For Stock Entry')
	
	def on_cancel(self):
		stock_entry = frappe.db.sql("""select name from `tabStock Entry`
			where pni_reference = %s and docstatus = 1""", self.name)
		if stock_entry:
			frappe.throw(_("Cannot cancel because submitted Stock Entry \
			{0} exists").format(stock_entry[0][0]))
		frappe.db.set(self, 'status', 'Cancelled')
		
		punch_table = frappe.get_doc("Punch Table",self.punch_table)
		punch_table.status = "In Stock"
		punch_table.save()
		
		bags = frappe.get_all("PNI Bag",{"reference":self.name})
		for bag in bags:
			bag_doc = frappe.get_doc("PNI Bag",bag.name)
			bag_doc.status = "Cancel"
			bag_doc.save()
			bag_doc.cancel()	
			self.cancel_reel_tracking(bag_doc.name)
	
	def manufacture_entry(self):
		return self.make_stock_entry()
	
	def make_stock_entry(self):
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.pni_reference_type = "Packing"
		stock_entry.pni_reference = self.name
		
		stock_entry.stock_entry_type = "Manufacture"
		stock_entry = self.set_se_items_finish(stock_entry)

		return stock_entry.as_dict()

	def set_se_items_finish(self, se):
		#set from and to warehouse
		se.from_warehouse = self.src_warehouse
		se.to_warehouse = self.fg_warehouse

		#get items to consume from previous stock entry or append to items
		#TODO allow multiple raw material transfer
		raw_material_cost = 0
		operating_cost = 0
		
		
		se = self.set_se_items(se, self.item, se.from_warehouse, None, False, reel_in= True)

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
		
		qty_of_total_production = float(qty_of_total_production) + self.total_weight
		
		# for item in self.coating_scrap:
		# 	if item.quantity > 0:
		# 		qty_of_total_production = float(qty_of_total_production + item.quantity)
		# 		if self.costing_method == "Relative Sales Value":
					# sale_value_of_pdt = frappe.db.get_value(
					# 	"Item Price", 
					# 	{
					# 		"item_code":item.item
					# 	}, 
					# 	"price_list_rate"
					# )
		# 			if sale_value_of_pdt:
		# 				total_sale_value += float(sale_value_of_pdt) * item.quantity
		# 			else:
		# 				frappe.throw(_("Selling price not set for item {0}").format(item.item))

		#add Stock Entry Items for produced goods and scrap
		se = self.set_se_items(
			se, 
			self.bag_item, 
			None, 
			se.to_warehouse, 
			True, 
			qty_of_total_production, 
			total_sale_value, 
			production_cost, 
			table_out = True
		)

		for item in self.packing_scrap:
			# if value_scrap:
				# se = self.set_se_items(
				# 	se, 
				# 	item, 
				# 	None, 
				# 	self.scrap_warehouse, 
				# 	True, 
				# 	qty_of_total_production, 
				# 	total_sale_value, 
				# 	production_cost
				# )
			# else:
			# 	se = self.set_se_items(se, item, None, self.scrap_warehouse, False)
			se = self.set_se_items(se, item, None, self.scrap_warehouse, False, scrap_item = True)

		return se
	
	def set_se_items(self, se, item, s_wh, t_wh, calc_basic_rate=False, 
		qty_of_total_production=None, total_sale_value=None, production_cost=None, 
		reel_in = False, table_out = False, scrap_item = False):
		# if item.quantity > 0:
		item_from_reel = {}
		class Empty:
			pass  
		if reel_in:			
			item_from_reel = Empty()
			item_from_reel.item = item
			item_from_reel.weight = self.weight
		if table_out:
			item_from_reel = Empty()
			item_from_reel.item = item
			item_from_reel.weight = self.total_weight
		if scrap_item:
			item_from_reel = Empty()
			item_from_reel.item = item.item
			item_from_reel.weight = item.qty

		expense_account, cost_center = frappe.db.get_values("Company", self.company, \
			["default_expense_account", "cost_center"])[0]
		item_name, stock_uom, description = frappe.db.get_values("Item", item_from_reel.item, \
			["item_name", "stock_uom", "description"])[0]

		item_expense_account, item_cost_center = frappe.db.get_value(
			"Item Default", 
			{
				'parent': item_from_reel.item, 
				'company': self.company
			},
			["expense_account", "buying_cost_center"]
		)

		if not expense_account and not item_expense_account:
			frappe.throw(
				_("Please update default Default Cost of Goods Sold Account for company {0}").format(self.company))

		if not cost_center and not item_cost_center:
			frappe.throw(_("Please update default Cost Center for company {0}").format(self.company))

		se_item = se.append("items")
		se_item.item_code = item_from_reel.item
		se_item.qty = item_from_reel.weight
		se_item.s_warehouse = s_wh
		se_item.t_warehouse = t_wh
		se_item.item_name = item_name
		se_item.description = description
		se_item.uom = stock_uom
		se_item.stock_uom = stock_uom

		se_item.expense_account = item_expense_account or expense_account
		se_item.cost_center = item_cost_center or cost_center

		# in stock uom
		se_item.transfer_qty = item_from_reel.weight
		se_item.conversion_factor = 1.00

		item_details = se.run_method( "get_item_details",args = (frappe._dict(
		{
			"item_code": item_from_reel.item, 
			"company": self.company, 
			"uom": stock_uom, 
			's_warehouse': s_wh
		})), for_update=True)

		for f in ("uom", "stock_uom", "description", "item_name", "expense_account",
		"cost_center", "conversion_factor"):
			se_item.set(f, item_details.get(f))

		if calc_basic_rate:
			se_item.basic_rate = production_cost/qty_of_total_production
			# if self.costing_method == "Physical Measurement":
			# 	se_item.basic_rate = production_cost/qty_of_total_production
			# elif self.costing_method == "Relative Sales Value":
			# 	sale_value_of_pdt = frappe.db.get_value("Item Price", 
			# 							{
			# 								"item_code":item_from_reel.item
			# 							}, "price_list_rate")
			# 	se_item.basic_rate=(float(sale_value_of_pdt)*float(production_cost))/float(total_sale_value)
		return se