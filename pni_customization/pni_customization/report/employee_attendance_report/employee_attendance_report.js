// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Attendance Report"] = {
	"filters": [
		{
			"fieldname": "shity_type", "fieldtype": "Select", "label": __("Shift Type"),
			"options": "\nDay Shift\nNight Shift"
		},
	]
};
