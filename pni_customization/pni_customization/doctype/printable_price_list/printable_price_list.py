# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class PrintablePriceList(Document):
    pass


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
			ip.customer is NULL
			and bgt.brand = ip.brand 
			and bg.name = bgt.parent
		group by ip.brand
    """)
