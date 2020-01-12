from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Other Reports"),
			"icon": "fa fa-list",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Items To Be Requested",
					"reference_doctype": "Item",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Item-wise Purchase History",
					"reference_doctype": "Item",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Material Requests for which Supplier Quotations are not created",
					"reference_doctype": "Material Request"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Address And Contacts",
					"label": _("Supplier Addresses And Contacts"),
					"reference_doctype": "Address",
					"route_options": {
						"party_type": "Supplier"
					}
				}
			]
		}
	]