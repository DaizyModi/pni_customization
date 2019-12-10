frappe.query_reports["Machine Design Report"] = {
	"filters": [
		{
			"fieldname": "employee", "fieldtype": "Link", "options": "Employee",  "label": __("Employee")
		},
		{
			"fieldname": "from_date", "fieldtype": "Date", "label": __("From Date")
		},
		{
			"fieldname": "to_date", "fieldtype": "Date", "label": __("To Date")
		}
	]
}
