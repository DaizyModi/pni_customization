# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DocumentReceived(Document):
	def on_submit(self):
		if self.pni_gate_entry:
			ge = frappe.get_doc("PNI Gate Entry", self.pni_gate_entry)
			if ge.docstatus != 1:
				frappe.throw("Gate Entry Not SUbmited Yet")
			if ge.entry_status == "Delivered":
				frappe.throw("This Gate Entry Already Delivered")
			ge.entry_status = "Delivered"
			ge.save(ignore_permissions=True)

	def on_cancel(self):
		if self.pni_gate_entry:
			ge = frappe.get_doc("PNI Gate Entry", self.pni_gate_entry)
			ge.entry_status = "Pending For Delivery "
			ge.save(ignore_permissions=True)