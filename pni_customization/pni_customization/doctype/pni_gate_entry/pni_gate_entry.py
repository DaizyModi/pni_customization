# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PNIGateEntry(Document):
	def validate(self):
		if self.gate_entry_type == "Document Receive":
			self.entry_status = "Pending For Delivery"
		else:
			self.entry_status = ""
		
		if not self.sender_names and self.gate_entry_type != "Visitor" :
				frappe.throw("Sender Name is Mandatory")
