# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UpdateShiftRequest(Document):
	def validate(self):
		if self.shift_type:
			for row in self.shift_employee_table:
				doc = frappe.get_doc({
					"doctype": "Shift Request",
					"shift_type": self.shift_type,
					"employee": row.employee
				})
				doc.insert()
			self.shift_type = ""
			self.shift_employee_table = ""
			frappe.msgprint("Updated")

