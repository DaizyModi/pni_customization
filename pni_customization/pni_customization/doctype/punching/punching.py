# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours

class Punching(Document):
	def validate(self):
		self.manage_table()
		if self.end_dt and self.start_dt:
			hours = time_diff_in_hours(self.end_dt, self.start_dt)
			frappe.db.set(self, 'operation_hours', hours)

	def onload(self):
		paper_blank_setting = frappe.get_doc("Paper Blank Settings","Paper Blank Settings")
		self.set_onload("scrapitemgroup", paper_blank_setting.punching_scrap)

	def manage_table(self):
		# setting = frappe.get_doc("PNI Settings","PNI Settings")
		for data in self.punching_table:
			reel_in = frappe.get_doc("Reel",data.reel_in)
			
			if not data.punch_table:
				doc = frappe.get_doc({
					"doctype": "Punch Table",
					"status": "Draft"
				})
				doc.insert()
				data.punch_table = doc.name
			else:
				doc = frappe.get_doc("Punch Table",data.punch_table)
			doc.custom_id = data.custom_id
			doc.item = data.item_out
			doc.printed_item = reel_in.printed_item
			doc.supplier_reel_id = reel_in.supplier_reel_id
			doc.punching_die = data.punching_die
			doc.brand = reel_in.brand
			doc.coated_reel = reel_in.coated_reel
			doc.printed_reel = reel_in.printed_reel
			doc.weight = data.weight_out
			doc.punching_die = data.punching_die
			doc.save()
	
	def manage_reel_tracking(self):
		for data in self.punching_table:
			doc = frappe.get_doc({
				"doctype": "Reel Tracking",
				"status": "Draft",
				"reel": data.reel_in,
				"reel_process": "Punching",
				"date": frappe.utils.nowdate(),
				"time": frappe.utils.nowtime(),
				"out_reel": data.punch_table,
				"status": "Punching Submit",
				"process_reference": self.name
			})
			doc.insert(ignore_permissions=True)
	
	def cancel_reel_tracking(self):
		for data in self.punching_table:
			doc = frappe.get_doc({
				"doctype": "Reel Tracking",
				"status": "Draft",
				"reel": data.reel_in,
				"reel_process": "Punching",
				"date": frappe.utils.nowdate(),
				"time": frappe.utils.nowtime(),
				"out_reel": data.punch_table,
				"status": "Punching Cancel",
				"process_reference": self.name
			})
			doc.insert(ignore_permissions=True)

	def on_submit(self):
		if (not self.end_dt) or (not self.end_dt):
			frappe.throw("Please Select Operation Start and End Time")
		for item in self.punching_table:
			if (not item.reel_in) or (not item.punch_table) :
				frappe.throw("Reel  and Punch Table is Compulsory")
		for data in self.punching_table:
			if not data.weight_out:
				frappe.throw("Weight Can't be empty")
			reel_in = frappe.get_doc("Reel",data.reel_in)
			reel_in.status = "Consume"
			reel_in.save()
			punch_table = frappe.get_doc("Punch Table",data.punch_table)
			punch_table.status = "In Stock"
			punch_table.save()
			punch_table.submit()
		self.manage_reel_tracking()
		frappe.db.set(self, 'status', 'Pending For Stock Entry')
	
	def on_cancel(self):
		stock_entry = frappe.db.sql("""select name from `tabStock Entry`
			where pni_reference = %s and docstatus = 1""", self.name)
		if stock_entry:
			frappe.throw(_("Cannot cancel because submitted Stock Entry \
			{0} exists").format(stock_entry[0][0]))
		frappe.db.set(self, 'status', 'Cancelled')
		for data in self.punching_table:
			reel_in = frappe.get_doc("Reel",data.reel_in)
			reel_in.status = "In Stock"
			reel_in.save()
			punch_table = frappe.get_doc("Punch Table",data.punch_table)
			punch_table.cancel()
		self.cancel_reel_tracking()
	
	def manufacture_entry(self):
		return self.make_stock_entry()
	
	def make_stock_entry(self):
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.pni_reference_type = "Punching"
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
		
		for item in self.punching_table:
			se = self.set_se_items(se, item, se.from_warehouse, None, False, reel_in= True)

		#TODO calc raw_material_cost

		#no timesheet entries, calculate operating cost based on workstation hourly rate and process start, end
		hourly_rate = frappe.db.get_value("Workstation", self.workstation, "hour_rate")
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
		for item in self.punching_table:
			if item.weight_out > 0:
				qty_of_total_production = float(qty_of_total_production) + item.weight_out
		
		# for item in self.coating_scrap:
		# 	if item.quantity > 0:
		# 		qty_of_total_production = float(qty_of_total_production + item.quantity)
		# 		if self.costing_method == "Relative Sales Value":
		# 			sale_value_of_pdt = frappe.db.get_value("Item Price", {"item_code":item.item}, "price_list_rate")
		# 			if sale_value_of_pdt:
		# 				total_sale_value += float(sale_value_of_pdt) * item.quantity
		# 			else:
		# 				frappe.throw(_("Selling price not set for item {0}").format(item.item))

		#add Stock Entry Items for produced goods and scrap
		for item in self.punching_table:
			se = self.set_se_items(se, item, None, se.to_warehouse, True, qty_of_total_production, total_sale_value, production_cost, table_out = True)

		for item in self.punching_scrap:
			# if value_scrap:
			# 	se = self.set_se_items(se, item, None, self.scrap_warehouse, True, qty_of_total_production, total_sale_value, production_cost)
			# else:
			# 	se = self.set_se_items(se, item, None, self.scrap_warehouse, False)
			se = self.set_se_items(se, item, None, self.scrap_warehouse, False, scrap_item = True)

		return se
	
	def set_se_items(self, se, item, s_wh, t_wh, calc_basic_rate=False, qty_of_total_production=None, total_sale_value=None, production_cost=None, reel_in = False, table_out = False, scrap_item = False):
		# if item.quantity > 0:
		item_from_reel = {}
		class Empty:
			pass  
		if reel_in:
			item_from_reel = frappe.get_doc("Reel",item.reel_in)
		if table_out:
			item_from_reel = frappe.get_doc("Punch Table",item.punch_table)
		if scrap_item:
			item_from_reel = Empty()
			item_from_reel.item = item.item
			item_from_reel.weight = item.qty

		expense_account, cost_center = frappe.db.get_values("Company", self.company, \
			["default_expense_account", "cost_center"])[0]
		item_name, stock_uom, description = frappe.db.get_values("Item", item_from_reel.item, \
			["item_name", "stock_uom", "description"])[0]

		item_expense_account, item_cost_center = frappe.db.get_value("Item Default", {'parent': item_from_reel.item, 'company': self.company},\
			["expense_account", "buying_cost_center"])

		if not expense_account and not item_expense_account:
			frappe.throw(_("Please update default Default Cost of Goods Sold Account for company {0}").format(self.company))

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
		{"item_code": item_from_reel.item, "company": self.company, "uom": stock_uom, 's_warehouse': s_wh})), for_update=True)

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

