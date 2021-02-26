# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class PrintablePriceList(Document):
    def validate(self):
        if self.paper_cup:
            for row in self.get('paper_cup_t'):
                data = get_price_list(row.brand)
                if data:
                    row.rate_per_piece = data[0][1]
                    row.price_1000 = data[0][2]
                    row.gst18 = data[0][3]
                    row.total_price = data[0][4]
                else:
                    return 0

        if self.paper_plate_bowl:
            for row in self.get('round_plate_t'):
                self.calculate_plate_bowl(row)
            for row in self.get('flower_plate_t'):
                self.calculate_plate_bowl(row)
            for row in self.get('heart_shape_plate_t'):
                self.calculate_plate_bowl(row)
            for row in self.get('square_plate_t'):
                self.calculate_plate_bowl(row)
            for row in self.get('square_bowl_t'):
                self.calculate_plate_bowl(row)
            for row in self.get('star_shape_t'):
                self.calculate_plate_bowl(row)

    def calculate_plate_bowl(self, row):
        data = get_item_price_list(row.item_code)
        if data:
            row.packet_price = data[0][1]
            if row.box_qty:
                row.box_price = (row.box_qty * row.packet_price)
            else:
                row.box_price = float(0)
        else:
            return 0


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
            and ip.brand = '{brand}'
			and bgt.brand = ip.brand 
			and bg.name = bgt.parent
            and ip.selling = 1
		group by ip.brand
    """.format(brand=brand))


@frappe.whitelist()
def get_item_price_list(item):
    return frappe.db.sql("""
        select 
			ip.item_code, (ip.price_list_rate * 1.18)
		from 
			`tabItem Price` as ip,
			`tabBrand Group Table` as bgt,
			`tabBrand Group` as bg
		where 
            ip.customer is NULL
            and ip.item_code = '{item}'
			and bgt.brand = ip.brand 
			and bg.name = bgt.parent
            and ip.selling = 1
		group by ip.brand
    """.format(item=item))
