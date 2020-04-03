# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	"""
	select 
    item as "Item:Link/Item:150", 
	count(item) as Nos, 
	sum(weight) as "Total Weight",
    status as "Status:Data:100", 
    size as "Size:Data:100", 
    gsm as "GSM:Data:100", 
    brand as "Brand:Link/Brand:100", 
    coated_reel as "Coated:Data:100", 
    printed_reel as "Printed:Data:100"      
    from `tabReel` 
        where docstatus = "1" and status = %(status)s 
    group by size, gsm, coated_reel, printed_reel;
	"""
	return columns, data
