frappe.query_reports["Reel Stock"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Draft\nIn Stock\nConsume\nSold",
			"default": "In Stock",
			"reqd": 1,
			"width": "80",
		},
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand",
			"reqd": 0,
			"width": "80",
		},
		{
			"fieldname":"gsm",
			"label": __("GSM"),
			"fieldtype": "Select",
			"options": "Draft\nIn Stock\nConsume\nSold",
			"default": "In Stock",
			"reqd": 1,
			"width": "80",
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Draft\nIn Stock\nConsume\nSold",
			"default": "In Stock",
			"reqd": 1,
			"width": "80",
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Draft\nIn Stock\nConsume\nSold",
			"default": "In Stock",
			"reqd": 1,
			"width": "80",
		},
	]
}