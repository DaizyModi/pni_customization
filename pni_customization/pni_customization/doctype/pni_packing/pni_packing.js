// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt
$(document).ready(function(){
	$("[data-fieldname='print_carton']").find("a.grey").click(function(event){
		event.preventDefault();
		// alert("The paragraph was clicked.");
	});
});
frappe.ui.form.on('PNI Packing', {
	refresh: function(frm){
		if(!frm.doc.__islocal && frm.doc.status == 'Pending For Stock Entry'){
			var finish_btn = frm.add_custom_button(__('Complete'), function(){
				process_production(frm);
			})
			finish_btn.addClass('btn-primary')
		}
	},
	packing_unit: function(frm){
		if(!frm.doc.packing_unit){
			frappe.msgprint("Item Don't have Default Selling UOM")
			frappe.model.set_value(frm.doctype,frm.docname, "conversation_factor",false)
		}else{
			frappe.call({
				"method": "get_conversation_factor",
				doc: cur_frm.doc,
				callback: function (r) {
					if(r.message){
	
						frappe.model.set_value(frm.doctype,frm.docname, "conversation_factor",r.message)
						refresh_field("conversation_factor");
					}	
				}
			})
		}
	},
	loose_stock: function(frm) {
	
	},
	onload: function(frm) {
		cur_frm.set_query("workstation", function() {
			return { filters: { papercup_forming_machine: 1 } };
		});
	},
	select_employee_group: function(frm) {
		frappe.call({
			"method": "get_employee_list",
			doc: cur_frm.doc,
			callback: function (r) {
				if(r.message){

					r.message.forEach(function(element) {
						var c = frm.add_child("employee");
						c.duty = element.duty;
						c.employee = element.employee;
					});
					refresh_field("employee");
				}	
			}
		})
	},
	refresh_carton_data: function(frm) {

	},
	enter_carton_weight: function(frm){
		
	}
})

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