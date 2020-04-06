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
					'filters': {"bag": true}
				}
			}
		},
		{
			"fieldname":"packing_category",
			"label": __("Packing Category"),
			"fieldtype": "Link",
			"options": "Packing Category",
			"reqd": 0,
			"width": "80"
		}
	]
}