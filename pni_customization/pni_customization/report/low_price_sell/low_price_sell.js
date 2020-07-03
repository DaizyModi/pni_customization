// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Low Price Sell"] = {
	"filters": [
		{
			"fieldname": "from_date", "fieldtype": "Date", "label": __("From Date")
		},
		{
			"fieldname": "to_date", "fieldtype": "Date", "label": __("To Date")
		},
		{
			"fieldname": "item_group", "fieldtype": "Link", "label": "Item Group", "options": "Item Group"
		}
	]
};
