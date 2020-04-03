# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class PNIMaterialTransfer(Document):
	def validate(self):
		self.total_weight = 0
		for item in self.material_transfer_table:
			self.total_weight += item.qty
	 
	def on_submit(self):
		count = 0
		for data in self.material_transfer_table:
			if data.item != self.item:
				frappe.throw("Invalid Bag/Reel")
			count += 1

		if count != self.nos:
			frappe.throw("Stock Not Available")
		
		for bag in self.material_transfer_table:
			doc = frappe.get_doc(bag.reference_type, bag.id)
			doc.warehouse = self.to_warehouse
			if self.is_wip_warehouse:
				doc.status = "Consume"
			doc.save()
		frappe.db.set(self, 'status', 'Pending For Stock Entry')
	
	def on_cancel(self):
		stock_entry = frappe.db.sql("""select name from `tabStock Entry`
			where pni_reference = %s and docstatus = 1""", self.name)
		if stock_entry:
			frappe.throw(_("Cannot cancel because submitted Stock Entry \
			{0} exists").format(stock_entry[0][0]))
		frappe.db.set(self, 'status', 'Cancelled')
		
		for bag in self.material_transfer_table:
			doc = frappe.get_doc(bag.reference_type, bag.id)
			doc.warehouse = self.from_warehouse
			doc.save()
	
	def get_bag(self):
		self.material_transfer_table = {}
		if self.pni_material_type=="Blank":
			bags = frappe.get_all("PNI Bag", filters={'item': self.item, 'status': "In Stock", 'warehouse': self.from_warehouse}, fields=['name', 'weight'])
			count = 0
			for bag in bags:
				count += 1
				if count > self.nos:
					break
				self.append("material_transfer_table",{"reference_type": "PNI Bag", "id": bag.name, "qty": bag.weight, "item":self.item})
			self.save()
		if self.pni_material_type=="Bottom":
			reels = frappe.get_all("Reel", filters={'item': self.item, 'status': "In Stock", 'warehouse': self.from_warehouse}, fields=['name', 'weight'])
			count = 0
			for reel in reels:
				count += 1
				if count > self.nos:
					break
				self.append("material_transfer_table",{"reference_type": "Reel", "id": reel.name, "qty": reel.weight, "item":self.item})
			self.save()
	def transfer_entry(self):
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.pni_reference_type = "PNI Material Transfer"
		stock_entry.pni_reference = self.name
		
		stock_entry.stock_entry_type = "Material Transfer"
		stock_entry = self.set_se_items_finish(stock_entry)

		return stock_entry.as_dict()

	def set_se_items_finish(self, se):
		#set from and to warehouse
		se.from_warehouse = self.from_warehouse
		se.to_warehouse = self.to_warehouse

		raw_material_cost = 0
		operating_cost = 0
		
		se = self.set_se_items(se, self.item, se.from_warehouse, se.to_warehouse, False)
		return se
	
	def set_se_items(self, se, item, s_wh, t_wh, calc_basic_rate=False, qty_of_total_production=None, total_sale_value=None, production_cost=None):
		# if item.quantity > 0:
		item_from_reel = {}
		class Empty:
			pass  
				
		item_from_reel = Empty()
		item_from_reel.item = self.item
		item_from_reel.weight = self.total_weight


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