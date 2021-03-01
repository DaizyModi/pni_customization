# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class ContractPaymentRequest(Document):
    def validate(self):
        if self.advance_payment_request:
            advance_request = frappe.get_all("Contract Payment Request", {
                                             'advance_payment_request': self.advance_payment_request})
            if advance_request:
                frappe.throw("A request already submitted once")

        if self.person_name:
            outstanding = frappe.db.sql(""" 
                select sum(cpr.paid_amount)
                    from
                        `tabContract Payment Request` as cpr
                    where
                        cpr.docstatus = 1
                        and cpr.person_name = '{emp}'
                    group by
                        cpr.person_name
            """.format(emp=self.person_name))

            if self.person_type == "Worker":
                total_amount = frappe.db.sql(""" 
                    select sum(pt.paying_amount)
                        from
                            `tabPacking Table` as pt, `tabPacking` as packing
                        where
                            packing.docstatus = 1
                            and pt.parent = packing.name
                            and pt.employee = '{emp}'
                        group by 
                            pt.employee,pt.item;
                """.format(emp=self.person_name))

            if total_amount and not outstanding:
                self.outstanding_amount = total_amount[0][0]
            elif total_amount and outstanding:
                self.outstanding_amount = total_amount[0][0] - \
                    outstanding[0][0]
            else:
                return 0
