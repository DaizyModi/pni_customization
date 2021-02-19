# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe.utils.nestedset import NestedSet, get_root_of
from erpnext import get_default_currency


class PurchaseExecutive(NestedSet):
    nsm_parent_field = 'parent_purchase_executive'

    def validate(self):
        if not self.parent_purchase_executive:
            if self.lft:
                self.nsm_parent_field = get_root_of('Purchase Executive')
        if self.employee:
            self.validate_employee_id()

    def update_nsm_model(self):
        frappe.utils.nestedset.update_nsm(self)

    def onload(self):
        self.load_dashboard_info()

    def load_dashboard_info(self):
        company_default_currency = get_default_currency()
        allocated_amount = frappe.db.sql(""" 
            select sum(grand_total) 
            from
                `tabPurchase Order`
            where
                docstatus=1 and purchase_executive = %s
        """, (self.name))

        print(allocated_amount[0][0])

        info = {}
        info['allocated_amount'] = flt(
            allocated_amount[0][0]) if allocated_amount else 0
        info['currency'] = company_default_currency

        self.set_onload('dashboard_info', info)

    # Validation for only single root node

    def on_update(self):
        super(PurchaseExecutive, self).on_update()
        self.validate_one_root()

    def get_email_id(self):
        if self.employee:
            user = frappe.db.get_value('Employee', self.employee, 'user_id')
            if not user:
                frappe.throw(
                    "User Id not set for Employee {0}". format(self.employee))
            else:
                return frappe.db.get_value("User", user, "email") or user

    def validate_employee_id(self):
        if self.employee:
            purchase_executive = frappe.db.get_value(
                "Purchase Executive", {'employee': self.employee})

            if purchase_executive and purchase_executive != self.name:
                frappe.throw("Another Purchase Executive {0} already exists with same Employee ID.".format(
                    purchase_executive))


def on_doctype_update():
    frappe.db.add_index("Purchase Executive", ['lft', 'rgt'])
