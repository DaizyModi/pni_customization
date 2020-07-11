# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "pni_customization"
app_title = "PNI Customization"
app_publisher = "Jigar Tarpara"
app_description = "PNI Customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "team@khatavahi.in"
app_license = "MIT"

# Includes in <head>
# ------------------
fixtures = [
	{
		"dt":"Custom Field", 
		"filters": [
			[
				"fieldname", "in", (
					"pni_sales_order", "pni_material_request", "pni_shift_order", "pni_user",
					"stack_size", "get_items_from",	"pni_sales_order_details", "get_pni_so",
					"pni_delivery_note", "pni_packing_table", "add_item_pni", "item_",
					"pni_material_type", "pni_qty_per_piece", "pni_inspection", "receiver_person",
					"pre_pni_inspection", "pni_programme_cycle_time", "pni_balance_qty", "scan_carton",
					"pni_attachment", "papercup_forming_machine", "warehouses_freshboxx", "src_warehouse",
					"fg_warehouse", "scrap_warehouse", "freshboxx_cb", "pni_paper_blank", "pni_reference_type",
					"pni_reference", "paper_blank_machine_type", "is_reel_item", "reel_item", "reel_table_purchase",
					"is_paper_plate", "paper_plate", "reel_item", "reel_brand", "reel_size", "reel_gsm",
					"total_reel_weight", "scrap_entry", "paper_cup", "paper_plate", "reel", "bag", "scan_bag",
					"scan_reel", "justdial_details", "j_leadid", "j_leadtype", "j_email", "j_date","j_category",
					"j_city","j_area","j_brancharea","j_dncmobile","j_dncphone","j_company", "j_pincode",
					"j_time","j_branchpin", "j_parentid","pni_sales_order_item","item_filter",
					"add_pni_bag", "weight_filter", "section_pni_settings", "section_pni_packing_table", "pni_clm_brk","is_paper_cup","base_uom_rate",
					"approve_law_rate__"
				)
			]
		]
	}
]

doc_events = {
 	"Stock Entry": {
        # "on_submit": "pni_customization.utils.validate_inspection_for_work_order",
		"validate": "pni_customization.utils.validate_stock_entry_item",
		"on_submit": "pni_customization.utils.manage_se_changes",
        "on_cancel": "pni_customization.utils.manage_se_changes"
    },
	"Item": {
		"on_update": "pni_customization.utils.update_item"
	},
	"Delivery Note": {
		"on_submit": "pni_customization.utils.submit_delivery_item",
        "on_cancel": "pni_customization.utils.cancel_delivery_item",
	},
	"Work Order": {
		"on_submit": "pni_customization.utils.submit_work_order_item",
		"validate": "pni_customization.utils.validate_work_order_item",
	},
	"Job Card": {
		"on_submit": "pni_customization.utils.job_card_submit",
		"on_update": "pni_customization.utils.job_card_update",
		# "validate": "pni_customization.utils.job_card_onload"
	},
	"Sales Order": {
		"validate": "pni_customization.utils.validate_so",
	},
	"Opportunity": {
		"validate": "pni_customization.utils.validate_opportunity"
	},
	"Purchase Order": {
		"validate": "pni_customization.utils.validate_po"
	},
	"Purchase Receipt": {
		"validate": "pni_customization.utils.validate_reel",
		"on_submit": "pni_customization.utils.create_reel",
		"on_cancel": "pni_customization.utils.cancel_reel"
	}
}
# include js, css files in header of desk.html
app_include_css = "assets/pni_customization/css/custom.css"
# app_include_js = "/assets/pni_customization/js/pni_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/pni_customization/css/pni_customization.css"
# web_include_js = "/assets/pni_customization/js/pni_customization.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

doctype_js = {
	"Sales Order" : "public/js/item_add.js",
	"Sales Invoice" : "public/js/item_add.js",
	"Purchase Order" : "public/js/item_add.js",
	"Purchase Invoice" : "public/js/item_add.js",
	"Quotation" : "public/js/item_add.js",
	"Work Order" : "public/js/item_add.js",
	"BOM" : "public/js/item_add.js",
	"Process Order" : "public/js/item_add.js",
	"Lead": "public/js/lead_customization.js",
	"Delivery Note": "public/js/delivery_note.js",
	"Opportunity": "public/js/opportunity.js",
	"Stock Entry" : "public/js/stock_entry.js",
}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "pni_customization.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "pni_customization.install.before_install"
# after_install = "pni_customization.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pni_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

permission_query_conditions = {
	"Lead": "pni_customization.utils.get_permission_query_conditions_for_lead",
	"Opportunity": "pni_customization.utils.get_permission_query_conditions_for_opportunity",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------
scheduler_events = {
	"all": [
		# "erpnext.stock.reorder_item.reorder_item"
	]
}
# scheduler_events = {
# 	"all": [
# 		"pni_customization.tasks.all"
# 	],
# 	"daily": [
# 		"pni_customization.tasks.daily"
# 	],
# 	"hourly": [
# 		"pni_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pni_customization.tasks.weekly"
# 	]
# 	"monthly": [
# 		"pni_customization.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "pni_customization.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pni_customization.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "pni_customization.task.get_dashboard_data"
# }

