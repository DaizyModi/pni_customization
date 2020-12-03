# -*- coding: utf-8 -*-
# Copyright (c) 2019, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PNIQualityInspection(Document):
	def on_submit(self):
		if self.reference_type == "Work Order" and self.reference_name:
			update_work_order(self.reference_name)
		if self.reference_type == "Job Card" and self.reference_name:
			update_job_card(self.reference_name)
	
	def validate(self):
		if self.reference_type == "Work Order" and self.reference_name:
			update_work_order(self.reference_name)
		self.total_qty = float(self.accepted_qty) + float(self.rejected_qty) + float(self.rework_qty)

def update_work_order(work_order):
	pni_qis =  frappe.get_all("PNI Quality Inspection",filters={"docstatus":1, "reference_type":"Work Order", "reference_name": work_order})
	rejected_qty = 0
	pni_rework_qty = 0
	for pni_qi in pni_qis:
		rejected_qty += int(frappe.get_value("PNI Quality Inspection",pni_qi.name, "rejected_qty"))
		pni_rework_qty += int(frappe.get_value("PNI Quality Inspection",pni_qi.name, "rework_qty"))
	frappe.db.set_value("Work Order", work_order, "pni_rejected_qty", rejected_qty, update_modified=False)
	frappe.db.set_value("Work Order", work_order, "pni_rework_qty", pni_rework_qty, update_modified=False)
	frappe.db.commit()

def update_job_card(job_card):
	pni_qis =  frappe.get_all("PNI Quality Inspection",filters={"docstatus":1, "reference_type":"Job Card", "reference_name": job_card})
	rejected_qty = 0
	pni_rework_qty = 0
	for pni_qi in pni_qis:
		rejected_qty += int(frappe.get_value("PNI Quality Inspection",pni_qi.name, "rejected_qty"))
		pni_rework_qty += int(frappe.get_value("PNI Quality Inspection",pni_qi.name, "rework_qty"))
	frappe.db.set_value("Job Card", job_card, "pni_rejected_qty", rejected_qty, update_modified=False)
	frappe.db.set_value("Job Card", job_card, "pni_rework_qty", pni_rework_qty, update_modified=False)
	frappe.db.commit()