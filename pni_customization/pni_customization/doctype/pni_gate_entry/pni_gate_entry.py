# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class PNIGateEntry(Document):
	def validate(self):
		if self.gate_entry_type == "Document Receive":
			self.entry_status = "Pending For Delivery"
			if not self.employee:
				frappe.throw("Employee is Mandatory")
		elif self.gate_entry_type == "Material Receipt":
			self.entry_status = "Pending For Delivery"
		else:
			self.entry_status = ""
		if (not self.sender_name1) and (self.gate_entry_type != "Visitor") :
			frappe.throw("Sender Name is Mandatory")
		
		if self.gate_entry_type == "Visitor" and get_datetime(self.in_time) > get_datetime(self.out_time):
			frappe.throw("In time must be less than to out time")