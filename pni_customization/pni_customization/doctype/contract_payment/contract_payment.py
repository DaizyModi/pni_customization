# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime


class ContractPayment(Document):
    def validate(self):
        self.validate_advance_payment_request()
        self.set_first_last_day()

        paid_amount = self.get_paid_amount()
        billing_total_amount = self.get_billing_amount()

        self.outstanding_amount = billing_total_amount - paid_amount

        if self.outstanding_amount <= 0:
            frappe.throw(
                "All dues paid against {0}".format(self.person_name))

        # self.allow_advance = self.calculate_paid_amount()

    def validate_advance_payment_request(self):
        if self.advance_payment_request:
            advance_request = frappe.get_all("Contract Payment", filters={
                'advance_payment_request': self.advance_payment_request, "person_name": self.person_name, 'name': ["!=", self.name], 'month': self.month, 'year': self.year})
            if advance_request:
                frappe.throw("A request already submitted once")

    def set_first_last_day(self):
        if self.month and self.year:
            first_day = frappe.utils.data.get_first_day(self.month)
            last_day = frappe.utils.data.get_last_day(self.month)
            self.from_date = str(first_day)
            self.to_date = str(last_day)

    def get_apr_by_month(self, doc):
        first_day = frappe.utils.data.get_first_day(self.month)
        last_day = frappe.utils.data.get_last_day(self.month)
        self.from_date = first_day
        self.to_date = last_day
        return str(first_day), str(last_day)

    def get_paid_amount(self):
        paid_amount = frappe.db.sql("""
            select sum(cpr.paid_amount)
                from
                    `tabContract Payment` as cpr
                where
                    cpr.docstatus = 1
                    and cpr.person_name = '{emp}'
                    and cpr.from_date >= '{start_date}'
                    and cpr.to_date <= '{end_date}'
                group by
                    cpr.person_name
        """.format(emp=self.person_name, start_date=self.from_date, end_date=self.to_date))
        paid_amount = paid_amount[0][0] if paid_amount else 0
        return paid_amount

    def get_billing_amount(self):
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
            """.format(emp=self.person_name, start_date=self.from_date, end_date=self.to_date))

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
            """.format(emp=self.person_name, start_date=self.from_date, end_date=self.to_date))
        billing_total_amount = billing_total_amount[0][0] if billing_total_amount else 0
        return billing_total_amount

    def on_submit(self):
        if self.payment_required_by:
            first_day_of_reqd_date = frappe.utils.data.get_first_day(
                self.payment_required_by)
            month = first_day_of_reqd_date.month
            year = first_day_of_reqd_date.year
            middle_date_obj = datetime.date(year, month, 20)
            middle_date = str(middle_date_obj)

            if self.payment_required_by <= middle_date:
                frappe.throw(
                    "Payment can't done before {0}".format(middle_date))

            if self.paid_amount > 0:
                if self.paid_amount > self.calculate_paid_amount():
                    frappe.throw("Paid amount can't be more than {0}".format(
                        self.calculate_paid_amount()))

        else:
            if self.paid_amount > 0:
                if self.paid_amount > self.outstanding_amount:
                    frappe.throw(
                        "Paid amount can't more than outstanding amount")

    def calculate_paid_amount(self):
        billing_amount = self.get_billing_amount_for_date()
        paid_amount = billing_amount * 0.6
        return paid_amount

    def get_billing_amount_for_date(self):
        if not self.month or not self.year:
            return 0
        first_day = frappe.utils.data.get_first_day(self.month)
        month = datetime.datetime.strptime(self.month, "%B")
        year = datetime.datetime.strptime(self.year, "%Y")
        middle_date_obj = datetime.date(year.year, month.month, 20)
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
