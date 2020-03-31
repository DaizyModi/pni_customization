frappe.query_reports["PNI Bag Stock"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Draft\nCancel\nIn Stock\nConsume\nSold",
			"default": "In Stock",
			"reqd": 1,
			"width": "80",
		},
		// {
		// 	"fieldname":"warehouse",
		// 	"label": __("Warehouse"),
		// 	"fieldtype": "Link",
		// 	"options": "Warehouse",
		// 	"reqd": 0,
		// 	"width": "80",
		// },
		// {
		// 	"fieldname":"item",
		// 	"label": __("Item"),
		// 	"fieldtype": "Link",
		// 	"options": "Item",
		// 	"reqd": 0,
		// 	"width": "80",
		// },
	]
}