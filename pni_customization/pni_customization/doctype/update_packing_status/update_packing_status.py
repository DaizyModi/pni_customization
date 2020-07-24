# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UpdatePackingStatus(Document):
	def validate(self):
		for row in self.packing_status:
			doc =  frappe.get_doc("PNI Carton", row.pni_carton)
			doc.status = row.status
			print(row.status)
			print(doc.status)
			doc.save()
		for row in self.packing_bag_status:
			doc =  frappe.get_doc("PNI Bag", row.pni_carton)
			doc.status = row.status
			doc.save()
		for row in self.pni_reel_status:
			doc =  frappe.get_doc("Reel", row.pni_carton)
			doc.status = row.status
			doc.save()
		frappe.db.commit()
		self.packing_status = []
		self.packing_bag_status = []
		self.pni_reel_status = []