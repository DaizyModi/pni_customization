# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime


class AdvanceContractPaymentRequest(Document):
    def validate(self):
        self.allow_advance = self.calculate_paid_amount()

    def calculate_paid_amount(self):
        billing_amount = self.get_billing_amount_for_date()
        paid_amount = billing_amount * 0.6
        return paid_amount

    def get_billing_amount_for_date(self):
        first_day = frappe.utils.data.get_first_day(self.payment_required_by)
        middle_date_obj = datetime.date(first_day.year, first_day.month, 20)
        last_day = str(middle_date_obj)
        if self.person_type == "Worker":
            billing_total_amount = frappe.db.sql("""
                    select sum(pt.paying_amount)
                        from
                            `tabPacking Table` as pt, `tabPacking` as packing
                        where
                            packing.docstatus = 1
                            and pt.parent = packing.name
                            and pt.employee = '{emp}'
                            and packing.date >= '{start_date}'
                            and packing.date <= '{end_date}'
                        group by
                            pt.employee;
                """.format(emp=self.person_name, start_date=first_day, end_date=last_day))

        if self.person_type == "Employee":
            billing_total_amount = frappe.db.sql("""
                    select sum(total_shift_stock * rate)
                        from
                            `tabPNI Packing`
                        where
                            docstatus = 1
                            and machine_helper_id = '{emp}'
                            and date >= '{start_date}'
                            and date <= '{end_date}'
                        group by
                            machine_helper_id;
                """.format(emp=self.person_name, start_date=first_day, end_date=last_day))
        billing_total_amount = billing_total_amount[0][0] if billing_total_amount else 0
        return billing_total_amount
