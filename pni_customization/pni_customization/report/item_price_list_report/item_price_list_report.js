// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Price List Report"] = {
	"filters": [
		{
			"fieldname": "brand_group", "fieldtype": "Link", "label": __("Brand Group"),
			"options": "Brand Group"
		},
	]
};
