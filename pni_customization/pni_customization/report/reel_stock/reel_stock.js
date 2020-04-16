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
            "fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
        },
		{
			"fieldname":"gsm",
			"label": __("GSM"),
			"fieldtype": "Data",
			"reqd": 0,
			"width": "80",
		},
		{
			"fieldname":"size",
			"label": __("Size"),
			"fieldtype": "Data",
			"reqd": 0,
			"width": "80",
		},
		{
			"fieldname":"coated",
			"label": __("Coated"),
			"fieldtype": "Select",
			"options": "All\nCoated\nUncoated",
			"default": "All",
			"reqd": 0,
			"width": "80",
		},
		{
			"fieldname":"printed",
			"label": __("Printed"),
			"fieldtype": "Select",
			"options": "All\nPrinted\nNon-Printed",
			"default": "All",
			"reqd": 0,
			"width": "80",
		}
	]
}