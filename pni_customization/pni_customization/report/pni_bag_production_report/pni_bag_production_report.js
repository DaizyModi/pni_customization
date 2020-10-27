// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PNI Bag Production Report"] = {
	"filters": [
		{
			"fieldname": "item", "fieldtype": "Link", "label": __("Item"), "options":"Item"
		},
		{
			"fieldname": "from_date", "fieldtype": "Date", "label": __("From Date")
		},
		{
			"fieldname": "to_date", "fieldtype": "Date", "label": __("To Date")
		}
	]
};
