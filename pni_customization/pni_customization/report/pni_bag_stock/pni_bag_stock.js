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
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"reqd": 0,
			"width": "80"
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