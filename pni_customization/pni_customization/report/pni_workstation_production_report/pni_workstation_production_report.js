// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PNI Workstation Production Report"] = {
	"filters": [
		{
			"fieldname": "from_date", "fieldtype": "Date", "label": __("From Date")
		},
		{
			"fieldname": "to_date", "fieldtype": "Date", "label": __("To Date")
		},
		{
			"fieldname": "item_group", "fieldtype": "Link", "label": __("Item Group"),"options":"Item Group","default":"Paper Cup"
		},
		{
			"fieldname": "workstation_head", "fieldtype": "Link", "label": __("Workstation Head"), "options":"Employee"
		},
		{
			"fieldname": "machine_helper", "fieldtype": "Link", "label": __("Machine Helper"), "options":"Employee"
		},
		{
			"fieldname": "workstation", "fieldtype": "Link", "label": __("Workstation"),"options":"Workstation"
		},
		{
			"fieldname": "shift", "fieldtype": "Select", "label": __("Shift"),"options":"\nDay\nNight"
		},
		{
			"fieldname": "employee", "fieldtype": "Link", "label": __("Employee"),"options":"Employee"
		},
		{
			"fieldname": "parent_item", "fieldtype": "Link", "label": __("Parent Item"),"options":"Item", get_query: () => {
				return {
					filters: {
						'has_variants': true
					}
				}
			}
		}
	]
};
