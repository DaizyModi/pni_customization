# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
from frappe.desk.form.linked_with import get_linked_doctypes

class GetApplicableForDoctypes(Document):
	def validate(self):
		if self.applicable_for:
			# get_applicable_for_doctype_list(self.applicable_for, "", searchfield, start, page_len, filters)
			linked_doctypes_map = get_linked_doctypes(self.applicable_for, True)

			linked_doctypes = []
			for linked_doctype, linked_doctype_values in linked_doctypes_map.items():
				linked_doctypes.append(linked_doctype)
				child_doctype = linked_doctype_values.get("child_doctype")
				if child_doctype:
					linked_doctypes.append(child_doctype)

			linked_doctypes += [self.applicable_for]

			linked_doctypes.sort()
			for dt in linked_doctypes:
				print(dt)
				self.append("applicable_for_table",{"name1":dt})
			print(linked_doctypes)
