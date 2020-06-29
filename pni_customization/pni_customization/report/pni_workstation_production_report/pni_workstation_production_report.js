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
