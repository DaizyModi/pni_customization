# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime


class ContractPayment(Document):
    def validate(self):
        if self.advance_payment_request:
            advance_request = frappe.get_all("Contract Payment", filters={
                'advance_payment_request': self.advance_payment_request, 'name': ["!=", self.name], 'month': self.month, 'year': self.year})
            print(advance_request)
            if advance_request:
                frappe.throw("A request already submitted once")

        if self.month and self.year:
            month = datetime.datetime.strptime(self.month, "%B")
            year = datetime.datetime.strptime(self.year, "%Y")
            first_day = frappe.utils.data.get_first_day(self.month)
            last_day = frappe.utils.data.get_last_day(self.month)
            self.from_date = str(first_day)
            self.to_date = str(last_day)

        if self.person_name:
            outstanding = frappe.db.sql("""
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

            if self.person_type == "Worker":
                total_amount = frappe.db.sql("""
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
                                pt.employee,pt.item;
                    """.format(emp=self.person_name, start_date=self.from_date, end_date=self.to_date))

            if self.person_type == "Employee":
                total_amount = frappe.db.sql("""
                    select sum(total_shift_stock * rate)
                        from
                            `tabPNI Packing` 
                        where 
                            docstatus = 1
                            and machine_helper_id = '{emp}'
                            and date >= '{start_date}'
                            and date <= '{end_date}'
                        group by
                            machine_helper_id, date
                """.format(emp=self.person_name, start_date=self.from_date, end_date=self.to_date))
                print(total_amount)

            if total_amount:
                if total_amount and not outstanding:
                    self.outstanding_amount = total_amount[0][0]
                elif total_amount and outstanding:
                    if total_amount[0][0] == outstanding[0][0]:
                        frappe.throw(
                            "All dues paid against {0}".format(self.person_name))
                    else:
                        self.outstanding_amount = total_amount[0][0] - \
                            outstanding[0][0]
                else:
                    return 0
            else:
                frappe.throw("No dues found")

    def on_submit(self):
        if self.payment_required_by:
            first_day_of_reqd_date = frappe.utils.data.get_first_day(
                self.payment_required_by)
            last_day_of_reqd_date = frappe.utils.data.get_last_day(
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
        per_day_amount = (self.outstanding_amount / 30) * 20
        paid_amount = per_day_amount * 0.6
        return paid_amount
