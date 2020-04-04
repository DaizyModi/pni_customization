# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
	columns, data = [], []
	return columns, data

"""select 
    item as "Item:Link/Item:150", 
    status as "Status:Data:100", 
    size as "Cups in Stack:Data:100", 
    no_of_stack as "Stack in Carton:Data:100", 
    count(item) as Nos, 
    sum(total) as "Total Cup",
    sum(net_weight) as "Net Weight",
    sum(gross_weight) as "Gross Weight"
        
    from `tabPNI Carton` 
        where docstatus = "1" and status = %(status)s  and is_paper_plate = ""
    group by item,size,no_of_stack, status;"""