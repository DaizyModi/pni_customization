# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class WorkstationPriceUpdateTool(Document):
	def get_workstation_list(self):
		filter = {}
		if self.department:
			filter['department'] = self.department
		doc = frappe.get_all("Workstation", filter, ["name","pni_rate"])
		return doc
	
	def validate(self):
		for row in self.workstation_price:
			workstation = frappe.get_doc("Workstation",row.workstation)
			workstation.pni_rate = row.pni_rate
			workstation.save()
		self.workstation_price = []
		self.department = ""
		frappe.msgprint("Workstation Price Updated!")

