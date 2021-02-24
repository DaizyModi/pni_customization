# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class PrintablePriceList(Document):
    def validate(self):
        for row in self.get('paper_cup_t'):
            data = get_price_list(row.brand)
            row.rate_per_piece = data[0][1]
            row.price_1000 = data[0][2]
            row.gst18 = data[0][3]
            row.total_price = data[0][4]


@frappe.whitelist()
def get_price_list(brand):

    return frappe.db.sql("""
		select 
			ip.brand, ip.price_list_rate, (ip.price_list_rate * bg.multiplier * 1000), (ip.price_list_rate * bg.multiplier * 1000 * 0.18), (ip.price_list_rate * bg.multiplier * 1000 * 1.18)
		from 
			`tabItem Price` as ip,
			`tabBrand Group Table` as bgt,
			`tabBrand Group` as bg
		where 
            1=1 
            and ip.brand = '{brand}'
			and bgt.brand = ip.brand 
			and bg.name = bgt.parent
            and ip.selling = 1
		group by ip.brand
    """.format(brand=brand))
