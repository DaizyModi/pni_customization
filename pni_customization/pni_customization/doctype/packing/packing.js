// Copyright (c) 2020, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Packing', {
	refresh: function(frm) {
		if(!frm.doc.__islocal && frm.doc.status == 'Pending For Stock Entry'){
			var finish_btn = frm.add_custom_button(__('Create Manufacture Entry'), function(){
				process_production(frm);
			});
			finish_btn.addClass('btn-primary')
		}
		
		if(!cur_frm.doc.__islocal){
			frm.set_query("item", "packing_scrap", function () {
				return {
					filters: {"item_group": frm.doc.__onload.scrapitemgroup}
				}
			});
		}
	},
	setup: function (frm) {
		// frm.set_query("workstation", function () {
		// 	return {
		// 		filters: {"paper_blank_machine_type": "Punching"}
		// 	}
		// });
		frm.set_query("punch_table", function () {
			return {
				filters: {"docstatus": 1, "status": "In Stock"}
			}
		});
	},
	pni_employee_group: function(frm){
		if(frm.doc.pni_employee_group){
			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "PNI Employee Group",
					name: frm.doc.pni_employee_group
				},
				callback: function (data) {
					
					frappe.model.set_value(frm.doctype,frm.docname, "fg_warehouse", data.message.fg_warehouse);
					frappe.model.set_value(frm.doctype,frm.docname, "scrap_warehouse", data.message.scrap_warehouse);
					frappe.model.set_value(frm.doctype,frm.docname, "src_warehouse", data.message.src_warehouse);
					
					data.message.pni_employee_table.forEach(function(data) {
						var c = frm.add_child("packing_table");
						c.employee = data.employee;
						c.emaployee_name = data.emaployee_name;
					})
					refresh_field("packing_table");
					
				}
			});
		}
	},
});

var process_production = function (frm) {
	frappe.call({
		doc: frm.doc,
		method: "manufacture_entry",
		// args:{
		// 	"status": status
		// },
		callback: function(r) {
			if (r.message){
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		}
	});
}