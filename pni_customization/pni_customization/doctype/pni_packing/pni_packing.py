# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class PNIPacking(Document):
	def validate(self):
		total = 0
		for row in self.items:
			total += int(row.total)
		total += int(self.total)
		self.total_stock = total
