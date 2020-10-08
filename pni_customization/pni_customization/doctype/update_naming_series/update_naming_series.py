# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UpdateNamingSeries(Document):
	pass

@frappe.whitelist()
def get_series():
	quury = frappe.db.sql("select name from `tabSeries` ")
	return {
		"series" : quury,
	}

@frappe.whitelist()
def get_count(prefix):
	count = frappe.db.get_value("Series",
				prefix, "current", order_by = "name")
	return count

@frappe.whitelist()
def update_count(prefix, count):
	if prefix:
		frappe.db.sql("update `tabSeries` set current = '{0}' where name = '{1}' ".format(count, prefix))
	frappe.msgprint("Success")
	return count

@frappe.whitelist()
def insert_series(series):
	"""insert series if missing"""
	if frappe.db.get_value('Series', series, 'name', order_by="name") == None:
		frappe.db.sql("insert into tabSeries (name, current) values (%s, 0)", (series))
		return "Series Added"
	else:
		return "Series Already There"