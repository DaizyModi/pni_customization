# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    data = get_data(filters)
    columns = get_columns()
    return columns, data

def get_columns():
    return  [
        {
            "fieldname": "item",
            "label": _("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "fieldname": "nos",
            "label": _("Nos"),
            "fieldtype": "Int",
        },
        {
            "fieldname": "total_weight",
            "label": _("Total Weight"),
            "fieldtype": "Float",
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "brand",
            "label": _("Brand"),
            "fieldtype": "Link",
            "options": "Brand"
        },
        {
            "fieldname": "coated_reel",
            "label": _("Coated Reel"),
            "fieldtype": "Check",
        },
        {
            "fieldname": "printed_reel",
            "label": _("Printed Reel"),
            "fieldtype": "Check",
        },
		{
            "fieldname": "warehouse",
            "label": _("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 120
        },
		{
            "fieldname": "actual_stock",
            "label": _("Actual Stock"),
            "fieldtype": "Float",
			"width": 100
        }
    ]

def get_data(filters=None):
	conditions = ""
	table = ""
	conditions_for_varient = ""

	if filters.gsm or filters.size:
		table += "`tabItem Variant Attribute` as ivt, "
		conditions_for_varient += " and ivt.parent = rl.item"


	if filters.status:
		conditions += " and rl.status = '{0}' ".format(filters.status)

	if filters.item:
		conditions += " and rl.item = '{0}' ".format(filters.item)

	if filters.brand:
		conditions += " and rl.brand = '{0}' ".format(filters.brand)

	if filters.gsm:
		conditions_for_varient += " and ivt.attribute = 'GSM' and ivt.attribute_value = '{0}' ".format(filters.gsm)

	if filters.size:
		conditions_for_varient += " and ivt.attribute = 'Reel Size' and ivt.attribute_value = '{0}' ".format(filters.size)


	if filters.warehouse:
		conditions += " and rl.warehouse = '{0}' ".format(filters.warehouse)

	if filters.coated == "Coated":
		conditions += " and rl.coated_reel <> '' "

	if filters.coated == "Uncoated":
		conditions += " and rl.coated_reel = '' "

	if filters.printed == "Printed":
		conditions += " and rl.printed_reel <> '' "

	if filters.printed == "Non-Printed":
		conditions += " and rl.printed_reel = '' "

	if filters.from_date:
		conditions += " and rl.creation >= '{0}' ".format(filters.from_date)

	if filters.to_date:
		conditions += " and rl.creation <='{0}' ".format(filters.to_date)
	return frappe.db.sql("""
		select 
		rl.item, count(rl.item), sum(rl.weight), rl.status, rl.brand, 
		rl.coated_reel, rl.printed_reel, rl.warehouse, bin.actual_qty

		from {0} `tabReel` as rl 
		left join
			`tabBin` as bin
		on bin.item_code = rl.item and bin.warehouse = rl.warehouse
		where rl.docstatus = '1' {1} {2}

		group by 
		rl.brand, rl.item, rl.coated_reel, rl.printed_reel, rl.warehouse;
	""".format(table, conditions, conditions_for_varient))