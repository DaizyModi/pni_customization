# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class BrandPricingUpdateTool(Document):
    def get_brand_list(self):
        if self.brand_group:
            doc = frappe.get_doc("Brand Group", self.brand_group)
            if doc:
                return doc.brand_group_table

    def get_brand_rate(self):
        data = {}
        for row in self.brand_pricing_table:
            value = frappe.db.get_value(
                "Item Price", {"brand": row.brand, "selling": True}, "price_list_rate")
            data[row.brand] = value
        return data

    def validate(self):
        doc = frappe.get_doc("Brand Group", self.brand_group)
        for row in self.brand_pricing_table:
            for row2 in doc.brand_group_table:
                if row2.brand == row.brand:
                    row2.selling_rate = row.selling_rate
        doc.save()
        frappe.db.commit()
        for row in self.brand_pricing_table:
            data = frappe.db.get_list(
                "Item Price", {"brand": row.brand, "selling": True})
            for item_price in data:
                ip = frappe.get_doc("Item Price", item_price.name)
                ip.price_list_rate = row.selling_rate
                ip.save()

        self.brand_pricing_table = []
        self.brand_group = ""
        frappe.db.commit()

        ppl_docs = frappe.get_all("Printable Price List")
        for ppl_doc in ppl_docs:
            ppl_ob = frappe.get_doc("Printable Price List", ppl_doc['name'])
            ppl_ob.save()
