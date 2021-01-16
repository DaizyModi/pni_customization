// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Machine Helper Payment"] = {
	"filters": [
		{
			"fieldname": "from_date", "fieldtype": "Date", "label": __("From Date")
		},
		{
			"fieldname": "to_date", "fieldtype": "Date", "label": __("To Date")
		},
		{
			"fieldname": "workstation_head", "fieldtype": "Data", "label": __("Workstation Head")
		},
	]
};
