# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours

class Coating(Document):
	def validate(self):
		self.manage_reel()
		if self.end_dt and self.start_dt:
			hours = time_diff_in_hours(self.end_dt, self.start_dt)
			frappe.db.set(self, 'operation_hours', hours)
		# self.calculate_ldap()

	def onload(self):
		paper_blank_setting = frappe.get_doc("Paper Blank Settings","Paper Blank Settings")
		self.set_onload("scrapitemgroup", paper_blank_setting.coating_scrap)

	def calculate_ldap(self):
		ldap = 0
		for data in self.coating_table:
			if float(data.gsm) >170:
				ldap += float(data.weight) * 0.08
			else:
				ldap += float(data.weight) * 0.08
		self.ldpe_bag = ldap
	
	def manage_reel(self):
		# setting = frappe.get_doc("PNI Settings","PNI Settings")
		for data in self.coating_table:
			reel_in = frappe.get_doc("Reel",data.reel_in)
			out_reel_relation = frappe.get_value("Reel Item Relation",
				{
					"in_item": reel_in.item, 
					"processtype": "Coating"
				}, 
				"out_item"
			)
			if not out_reel_relation:
				frappe.throw("Reel Item Relation Missing for Item "+reel_in.item)
			if not data.reel_out:
				doc = frappe.get_doc({
					"doctype": "Reel",
					"status": "Draft",
					"process_prefix": "CO",
					"supplier_reel_id": reel_in.supplier_reel_id,
					"item": out_reel_relation,
					"type": reel_in.type,
					"brand": reel_in.brand,
					"size": reel_in.size,
					"coated_reel": True,
					"printed_reel": reel_in.printed_reel,
					"gsm": reel_in.gsm,
					"weight": data.weight_out
				})
				doc.insert()
				data.reel_out = doc.name
			else:
				doc = frappe.get_doc("Reel",data.reel_out)
				doc.reel_id = data.reel_id,
				doc.weight = data.weight_out
				doc.save()
	
	def manage_reel_tracking(self):
		# setting = frappe.get_doc("PNI Settings","PNI Settings")
		
		for data in self.coating_table:
			doc = frappe.get_doc({
				"doctype": "Reel Tracking",
				"status": "Draft",
				"reel": data.reel_in,
				"reel_process": "Coating",
				"date": frappe.utils.nowdate(),
				"time": frappe.utils.nowtime(),
				"out_reel": data.reel_out,
				"status": "Coating Submit",
				"process_reference": self.name
			})
			doc.insert(ignore_permissions=True)
	
	def cancel_reel_tracking(self):
		# setting = frappe.get_doc("PNI Settings","PNI Settings")
		
		for data in self.coating_table:
			doc = frappe.get_doc({
				"doctype": "Reel Tracking",
				"status": "Draft",
				"reel": data.reel_in,
				"reel_process": "Coating",
				"date": frappe.utils.nowdate(),
				"time": frappe.utils.nowtime(),
				"out_reel": data.reel_out,
				"status": "Coating Cancel",
				"process_reference": self.name
			})
			doc.insert(ignore_permissions=True)

	def on_submit(self):
		if (not self.end_dt) or (not self.end_dt):
			frappe.throw("Please Select Operation Start and End Time")
		for item in self.coating_table:
			if (not item.reel_in) or (not item.reel_out) :
				frappe.throw("Reel is Compulsory")
		for data in self.coating_table:
			if not data.weight_out:
				frappe.throw("Weight Can't be empty")
			reel_in = frappe.get_doc("Reel",data.reel_in)
			reel_in.status = "Consume"
			reel_in.save()
			reel_out = frappe.get_doc("Reel",data.reel_out)
			reel_out.status = "In Stock"
			reel_out.save()
			reel_out.submit()
		self.manage_reel_tracking()
		frappe.db.set(self, 'status', 'Pending For Stock Entry')
	
	def on_cancel(self):
		stock_entry = frappe.db.sql("""select name from `tabStock Entry`
			where pni_reference = %s and docstatus = 1""", self.name)
		if stock_entry:
			frappe.throw(_("Cannot cancel because submitted Stock Entry \
			{0} exists").format(stock_entry[0][0]))
		frappe.db.set(self, 'status', 'Cancelled')
		for data in self.coating_table:
			reel_in = frappe.get_doc("Reel",data.reel_in)
			reel_in.status = "In Stock"
			reel_in.save()
			reel_out = frappe.get_doc("Reel",data.reel_out)
			reel_out.cancel()
		self.cancel_reel_tracking()
	
	def manufacture_entry(self, status):
		return self.make_stock_entry(status)
	
	def make_stock_entry(self, status):
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.pni_reference_type = "Coating"
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

		for item in self.coating_table:
			se = self.set_se_items(se, item, se.from_warehouse, None, False, reel_in= True)
		if self.ldpe_bag>0:
			pass
			# paper_blank_setting = frappe.get_doc("Paper Blank Settings","Paper Blank Settings")
			# se = self.set_se_items(se, paper_blank_setting.ldpe_bag, 
			# se.from_warehouse, None, False, ldpe=True)
		#TODO calc raw_material_cost

		#no timesheet entries, calculate operating cost 
		# based on workstation hourly rate and process start, end
		hourly_rate = frappe.db.get_value("Workstation", self.work_station, "hour_rate")
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
		for item in self.coating_table:
			if item.weight_out > 0:
				qty_of_total_production = float(qty_of_total_production) + item.weight_out
		
		# for item in self.coating_scrap:
		# 	if item.quantity > 0:
		# 		qty_of_total_production = float(qty_of_total_production + item.quantity)
		# 		if self.costing_method == "Relative Sales Value":
		# 			sale_value_of_pdt = frappe.db.get_value("Item Price", 
		# 				{"item_code":item.item}, "price_list_rate")
		# 			if sale_value_of_pdt:
		# 				total_sale_value += float(sale_value_of_pdt) * item.quantity
		# 			else:
		# 				frappe.throw(_("Selling price not set for item {0}").format(item.item))

		#add Stock Entry Items for produced goods and scrap
		for item in self.coating_table:
			se = self.set_se_items(se, item, None, se.to_warehouse, True, 
					qty_of_total_production, total_sale_value, 
					production_cost, reel_out = True)

		for item in self.coating_scrap:
			# if value_scrap:
			# 	se = self.set_se_items(se, item, None, self.scrap_warehouse, True, 
			# qty_of_total_production, total_sale_value, production_cost)
			# else:
			# 	se = self.set_se_items(se, item, None, self.scrap_warehouse, False)
			se = self.set_se_items(se, item, None, self.scrap_warehouse, 
					False, scrap_item = True)

		return se
	
	def set_se_items(self, se, item, s_wh, t_wh, calc_basic_rate=False, 
		qty_of_total_production=None, total_sale_value=None, production_cost=None, 
		reel_in = False, reel_out = False, scrap_item = False, ldpe = False):
		# if item.quantity > 0:
		item_from_reel = {}
		class Empty:
			pass  
		if reel_in:
			item_from_reel = frappe.get_doc("Reel",item.reel_in)
		if reel_out:
			item_from_reel = frappe.get_doc("Reel",item.reel_out)
		if scrap_item:
			item_from_reel = Empty()
			item_from_reel.item = item.item
			item_from_reel.weight = item.qty
		if ldpe:
			item_from_reel = Empty()
			item_from_reel.item = item
			item_from_reel.weight = self.ldpe_bag
		expense_account, cost_center = frappe.db.get_values("Company", self.company, \
			["default_expense_account", "cost_center"])[0]
		item_name, stock_uom, description = frappe.db.get_values("Item", item_from_reel.item, \
			["item_name", "stock_uom", "description"])[0]

		item_expense_account, item_cost_center = frappe.db.get_value("Item Default", 
			{
				'parent': item_from_reel.item, 
				'company': self.company
			},\
			["expense_account", "buying_cost_center"])

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
				"s_warehouse": s_wh})), for_update=True)

		for f in ("uom", "stock_uom", "description", "item_name", "expense_account",
		"cost_center", "conversion_factor"):
			se_item.set(f, item_details.get(f))

		if calc_basic_rate:
			se_item.basic_rate = production_cost/qty_of_total_production
			# if self.costing_method == "Physical Measurement":
			# 	se_item.basic_rate = production_cost/qty_of_total_production
			# elif self.costing_method == "Relative Sales Value":
			# 	sale_value_of_pdt = frappe.db.get_value("Item Price", 
			# 		{"item_code":item_from_reel.item}, "price_list_rate")
			# 	se_item.basic_rate = (
			# 		float(sale_value_of_pdt) 
			# 		* float(production_cost)) / float(total_sale_value)
		return se
