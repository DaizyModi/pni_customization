# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
from frappe.core.doctype.user_permission.user_permission import get_applicable_for_doctype_list

class GetApplicableForDoctypes(Document):
	def validate(self):
		if self.applicable_for:
			pass
			# get_applicable_for_doctype_list(self.applicable_for, "", searchfield, start, page_len, filters)
