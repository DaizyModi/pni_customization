from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Work Flow"),
			"items": [
                {
					"type": "doctype",
					"name": "PNI Sales Order",
					"description": _("Initial Order From Customer"),
				},
				{
					"type": "doctype",
					"name": "Sales Order",
					"description": _("ERPNext Sales Order"),
				},
				{
					"type": "doctype",
					"name": "PNI Packing",
					"description": _("PNI Packing"),
				},
				
			]
		},
		{
			"label": _("Production"),
			"items": [
				{
					"type": "doctype",
					"name": "Shift Order",
					"description": _("Employee Shift Order."),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"description": _("Record item movement."),
				},
				{
					"type": "doctype",
					"name": "PNI Material Request",
					"description": _("Requests for items."),
				},
				{
					"type": "doctype",
					"name": "Reel Tracking",
					"description": _("Reel Tracking Module."),
				},
			]
		},
		{
			"label": _("Office Use"),
			"items": [
                {
					"type": "doctype",
					"name": "PNI Gate Entry",
					"description": _("Initial Order From Customer"),
				},
				{
					"type": "doctype",
					"name": "PNI Gate Pass",
					"description": _("Initial Order From Customer"),
				}
			]
		},
        {
			"label": _("Process Manufacturing"),
			"items": [
				{
					"type": "doctype",
					"name": "Process Definition",
					"description": _("Process Definition."),
				},
				{
					"type": "doctype",
					"name": "Process Type",
					"description": _("Process Type."),
				},
                {
					"type": "doctype",
					"name": "Manufacturing Department",
					"description": _("Manufacturing Department"),
				},
                {
					"type": "doctype",
					"name": "Item",
					"description": _("All Products or Services."),
				},
                {
					"type": "doctype",
					"name": "Batch",
					"description": _("Batch (lot) of an Item."),
				},
			]
		},
	]
