// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Paper Plate Stock"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Available\nPending\nDelivered",
			"default": "Available",
			"reqd": 1,
			"width": "80",
		},
		,
		{
			"fieldname":"item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"reqd": 0,
			"width": "80",
		},
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand",
			"reqd": 0,
			"width": "80",
			"get_query": function(){ 
				return {
					'filters': {"paper_plate": true}
				}
			}
		},
		{
			"fieldname": "from_date", "fieldtype": "Date", "label": __("From Date")
		},
		{
			"fieldname": "to_date", "fieldtype": "Date", "label": __("To Date")
		}
		// {
		// 	"fieldname":"gsm",
		// 	"label": __("GSM"),
		// 	"fieldtype": "Float",
		// 	"reqd": 0,
		// 	"width": "80",
		// },
		// {
		// 	"fieldname":"size",
		// 	"label": __("Size"),
		// 	"fieldtype": "Float",
		// 	"reqd": 0,
		// 	"width": "80",
		// },
		// {
		// 	"fieldname":"coated",
		// 	"label": __("Coated"),
		// 	"fieldtype": "Check",
		// 	"reqd": 0,
		// 	"width": "80",
		// },
		// {
		// 	"fieldname":"printed",
		// 	"label": __("Printed"),
		// 	"fieldtype": "Check",
		// 	"reqd": 0,
		// 	"width": "80",
		// }
	]
}