# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class UpdateShiftRequest(Document):
    def validate(self):
        if self.shift_type:
            for row in self.shift_employee_table:
                doc = frappe.get_doc({
                    "doctype": "Shift Request",
                    "shift_type": self.shift_type,
                    "employee": row.employee,
                    "from_date": self.from_date,
                    "to_date": self.to_date
                })
                doc.insert()
            self.from_date = ""
            self.to_date = ""
            self.shift_type = ""
            self.shift_employee_table = ""
            self.start_time = ""
            self.end_time = ""
            frappe.msgprint("Updated")


@frappe.whitelist()
def get_employees(shift_type):
    return frappe.db.sql(""" 
        select emp.name from 
            `tabEmployee` as emp, 
            `tabEmployee Shift Type` as est 
        where 
        emp.name = est.parent 
        and est.shift_type = '{shift_type}'
        order by emp.name;
    """.format(shift_type=shift_type))
