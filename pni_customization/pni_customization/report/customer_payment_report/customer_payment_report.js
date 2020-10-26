// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Payment Report"] = {
	"filters": [
		{
			"fieldname": "from_date", "fieldtype": "Date", "label": __("From Date")
		},
		{
			"fieldname": "to_date", "fieldtype": "Date", "label": __("To Date")
		},
		{
			"fieldname": "workstation_head", "fieldtype": "Link", "label": __("Workstation Head"), "options": "Employee"
		},
		{
			"fieldname": "workstation", "fieldtype": "Link", "label": __("Workstation"), "options": "Workstation"
		},
		{
			"fieldname": "shift", "fieldtype": "Select", "label": __("Shift"), "options": "\nDay\nNight"
		},
	]
};
