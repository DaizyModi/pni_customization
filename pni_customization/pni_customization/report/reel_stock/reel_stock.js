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
		,
		{
			"fieldname":"item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"reqd": 0,
			"width": "80",
		},
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand",
			"reqd": 0,
			"width": "80",
			"get_query": function(){ 
				return {
					'filters': {"reel": true}
				}
			}
		},
		{
			"fieldname":"gsm",
			"label": __("GSM"),
			"fieldtype": "Float",
			"reqd": 0,
			"width": "80",
		},
		{
			"fieldname":"size",
			"label": __("Size"),
			"fieldtype": "Float",
			"reqd": 0,
			"width": "80",
		},
		{
			"fieldname":"coated",
			"label": __("Coated"),
			"fieldtype": "Check",
			"reqd": 0,
			"width": "80",
		},
		{
			"fieldname":"printed",
			"label": __("Printed"),
			"fieldtype": "Check",
			"reqd": 0,
			"width": "80",
		}
	]
}