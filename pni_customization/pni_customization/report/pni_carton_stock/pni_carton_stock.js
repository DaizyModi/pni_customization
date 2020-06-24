frappe.query_reports["PNI Carton Stock"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Pending\nAvailable\nDelivered",
			"default": "Available",
			"reqd": 1,
			"width": "80",
		}
	]
}