from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Engineering"),
			"items": [
				{
					"type": "doctype",
					"name": "Work Order",
					"description": _("Work Order")
				},
				{
					"type": "doctype",
					"name": "Job Card",
					"description": _("Job Card")
				},
				{
					"type": "doctype",
					"name": "Operation",
					"description": _("Operation"),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"description": _("Record item movement."),
				},
				{
					"type": "doctype",
					"name": "Get Applicable For Doctypes",
					"description": _("Usefull for User Permission"),
				}
			]
		},
		{
			"label": _("Paper Cup Making"),
			"items": [
				{
					"type": "doctype",
					"name": "Brand Pricing Update Tool For Customer",
					"description": _("Brand Pricing Update Tool For Customer"),
				},
				{
					"type": "doctype",
					"name": "Workstation Price Update Tool",
					"description": _("Workstation Price Update Tool"),
				},
				{
					"type": "doctype",
					"name": "Brand Pricing Update Tool",
					"description": _("Brand Pricing Update Tool"),
				},
				{
					"type": "doctype",
					"name": "Brand Group",
					"description": _("Brand Group"),
				},
				{
					"type": "doctype",
					"name": "PNI Packing",
					"description": _("Detail of Paper Cup Carton"),
				},
				{
					"type": "doctype",
					"name": "Process Order",
					"description": _(" Record Production Detail")
				},
				{
					"type": "doctype",
					"name": "PNI Carton",
					"description": _("Carton Details"),
				},
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
					"name": "PNI Material Transfer",
					"description": _("PNI Material Transfer"),
				}
			]
		},
		{
			"label": _("Paper Cup Reports"),
			"items": [
				{
					"type": "report",
					"name": "Workstation Scrap",
					"description": _("Workstation Scrap"),
					"is_query_report": True,
					"reference_doctype": "PNI Packing",
				},
				{
					"type": "report",
					"name": "Machine Helper Payment",
					"description": _("Machine Helper Payment"),
					"is_query_report": True,
					"reference_doctype": "PNI Packing",
				},
				{
					"type": "report",
					"name": "Packing Payment Reort",
					"description": _("Packing Payment Report"),
					"is_query_report": True,
					"reference_doctype": "PNI Packing",
				},
				{
					"type": "report",
					"name": "Item Price List Report",
					"description": _("Item Price List Report"),
					"is_query_report": True,
					"reference_doctype": "Item Price",
				},
                {
					"type": "report",
					"name": "Paper Cup Stock",
					"description": _("Paper Cup Stock"),
					"is_query_report": True,
					"reference_doctype": "PNI Carton",
				},
				{
					"type": "report",
					"name": "PNI Workstation Production Report",
					"description": _("PNI Workstation Production Report"),
					"is_query_report": True,
					"reference_doctype": "PNI Packing",
				},
				{
					"type": "report",
					"name": "Paper Plate Stock",
					"description": _("Paper Plate Stock"),
					"is_query_report": True,
					"reference_doctype": "PNI Carton",
				},
				{
					"type": "report",
					"name": "Reel Stock",
					"description": _("Reel Stock"),
					"is_query_report": True,
					"reference_doctype": "Reel",
				},
				{
					"type": "report",
					"name": "PNI Bag Stock",
					"description": _("PNI Bag Stock"),
					"is_query_report": True,
					"reference_doctype": "PNI Bag",
				},
				{
					"type": "report",
					"name": "Low Price Sell",
					"description": _("Low Price Sell"),
					"is_query_report": True,
					"reference_doctype": "Sales Order",
				},
				{
					"type": "report",
					"name": "PNI Production Plan Detail",
					"description": _("PNI Production Plan Detail"),
					"is_query_report": True,
					"reference_doctype": "Sales Order",
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Employee Attendance Report",
					"doctype": "Attendance Log"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "PNI Carton Packing",
					"doctype": "PNI Carton"
				}
			]
		},
		{
			"label": _("Paper Blank Processing"),
			"items": [
				{
					"type": "doctype",
					"name": "Coating",
					"description": _("Coating Details"),
				},
				{
					"type": "doctype",
					"name": "Slitting",
					"description": _("Slitting Details"),
				},
				{
					"type": "doctype",
					"name": "Printing",
					"description": _("Printing Details"),
				},
				{
					"type": "doctype",
					"name": "Printing Cylinder",
					"description": _("Printing Cylinder Master"),
				},
				{
					"type": "doctype",
					"name": "Punching",
					"description": _("Punching Master"),
				},
				{
					"type": "doctype",
					"name": "Packing",
					"description": _("Packing"),
				},
				{
					"type": "doctype",
					"name": "Punch Table",
					"description": _("Punched Table Master"),
				},
				{
					"type": "doctype",
					"name": "Punching Die",
					"description": _("Punching Die Master"),
				},
				{
					"type": "doctype",
					"name": "Reel",
					"description": _("Reel Master"),
				},
				{
					"type": "doctype",
					"name": "Reel Tracking",
					"description": _("Reel History Tracking"),
				}
			]
		},
		{
			"label": _("Sales"),
			"items": [
				{
					"type": "doctype",
					"name": "Lead",
					"description": _("Description")
				},
				{
					"type": "doctype",
					"name": "Opportunity",
					"description": _("Opportunity")
				},
				{
					"type": "doctype",
					"name": "PNI Quotation",
					"description": _("PNI Quotation")
				},
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
					"type": "report",
					"name": "Sales Person Account Receivable",
					"description": _("Sales Person Account Receivable"),
					"is_query_report": True,
					"reference_doctype": "Sales Invoice",
				},
				{
					"type": "report",
					"name": "Sales Person Sales Analytics",
					"description": _("Sales Person Sales Analytics"),
					"is_query_report": True,
					"reference_doctype": "Sales Order",
				}
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
				},
				{
					"type": "doctype",
					"name": "Document Received",
					"description": _("Document Received"),
				},
				{
					"type": "doctype",
					"name": "PNI Gate Exit",
					"description": _("PNI Gate Exit"),
				}
			]
		}
	]
