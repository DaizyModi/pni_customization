# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Coating(Document):
	def on_submit(self):
		# if not self.fg_warehouse:
		# 	frappe.throw(_("Target Warehouse is required before Submit"))
		# if self.scrap and not self.scrap_warehouse:
		# 	frappe.throw(_("Scrap Warehouse is required before submit"))
		# for item in self.materials:
		# 	if item.quantity == 0:
		# 		frappe.throw(_("Raw Material can't be zero for item {0}".format(item.item)))
		# for item in self.finished_products:
		# 	if item.quantity == 0:
		# 		frappe.throw(_("Raw Material can't be zero for item {0}".format(item.item)))
		frappe.db.set(self, 'status', 'Pending For Stock Entry')
	
	def manufacture_entry(self, status):
		# if status == "In Process":
		# 	if not self.end_dt:
		# 		self.end_dt = get_datetime()
		# self.flags.ignore_validate_update_after_submit = True
		# self.save()
		return self.make_stock_entry(status)
	
	def make_stock_entry(self, status):
		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.process_order = self.name

		if status == "In Process":
			stock_entry.stock_entry_type = "Manufacture"
			stock_entry = self.set_se_items_finish(stock_entry)

		return stock_entry.as_dict()
