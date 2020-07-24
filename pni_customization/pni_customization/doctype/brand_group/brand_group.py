# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class BrandGroup(Document):
	def validate(self):
		query = ""
		for data in self.brand_group_table:
			query += "'"+data.brand + "',"
		self.query = query.strip(",")