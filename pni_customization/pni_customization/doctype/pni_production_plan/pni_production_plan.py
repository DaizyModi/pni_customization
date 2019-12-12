# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PNIProductionPlan(Document):

	def onload(self):
		row_carton = []
		self.production_plan_stock = {}
		for row in self.production_so:
			if row.item not in row_carton:
				row_carton.append(row.item)
				pni_so = frappe.db.sql("""
					select count(name) from `tabPNI Carton` where status = "Available" and docstatus="1" and item = "{0}"
				""".format(row.item))
				self.append("production_plan_stock",{
					"item": row.item,
					"available_carton": int(pni_so[0][0]), # - int(self.get_reserve(row.item)),
					# "reserve_carton": self.get_reserve(row.item)
				})

	def get_reserve(self, item):
		pni_so = frappe.db.sql("""
					select sum(reserve_carton) from `tabProduction SO Table` where item = "{0}" 
				""".format(item))
		return pni_so[0][0]
	def get_pni_so(self):
		condition = ""
		if self.customer:
			condition += " and so.customer = '" + self.customer + "'"
		
		if self.from_posting_date and self.to_posting_date:
			condition += " and so.date >= '" + self.from_posting_date + "'"
			condition += " and so.date <= '" + self.to_posting_date + "'"
			
		if self.from_delivery_date and self.to_delivery_date:
			condition += " and so.delivery_date >= '" + self.from_delivery_date + "'"
			condition += " and so.delivery_date <= '" + self.to_delivery_date + "'"
		
		if self.item:
			condition += " and soi.item = '"+self.item + "'"
			
		pni_so = frappe.db.sql("""
			select 
				so.name, soi.item, soi.qty, soi.name from `tabPNI Sales Order` as so 
					inner join 
				`tabPNI Sales Order Item` as soi on soi.parent = so.name 
				where 1=1 {0}
			""".format(condition))
		self.production_so = {}
		for row in pni_so:
			if not self.is_planed(row[3]):
				self.append('production_so', {
					"sales_order": row[0],
					"item": row[1],
					"order_carton": row[2],
					"pni_sales_order_item": row[3]
				})
		self.save()
	
	def  is_planed(self, so_item_name):
		pni_plan = frappe.db.sql("""
			select name from `tabProduction SO Table`  where pni_sales_order_item = '{0}'
		""".format(so_item_name))
		return pni_plan

@frappe.whitelist()
def make_joborder(source_name, target_doc=None, ignore_permissions = False):	
	doclist = get_mapped_doc("PNI Production Plan", source_name, {
			"PNI Production Plan": {
				"doctype": "Paper Cup Job Order",
				"field_map": {
					"name" : "pni_production_plan",
					"customer": "party",
				}
			},
			"Production SO Table": {
				"doctype": "Paper Cup Job Order Item",
				"field_map": {
					"item" : "item",
					"manufacture_carton": "carton",
				}
			}
		}, target_doc, ignore_permissions=ignore_permissions)
	
	return doclist