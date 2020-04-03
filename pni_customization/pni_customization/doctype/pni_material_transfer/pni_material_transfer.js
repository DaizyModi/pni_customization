// Copyright (c) 2020, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Material Transfer', {
	refresh: function (frm) {
		frm.set_query("reference_type", "material_transfer_table", function () {
			return {
				filters: {"name": "PNI Bag"}
			}
		});
		frm.set_query("item", function () {
			return {
				filters: [
					["pni_material_type", "in", "Blank,Bottom"]
				]
			}
		});
		if(!frm.doc.__islocal && frm.doc.status == 'Pending For Stock Entry'){
			var finish_btn = frm.add_custom_button(__('Create Transfer Entry'), function(){
				tarnsfer_entry(frm);
			});
			finish_btn.addClass('btn-primary')
		}
	},
	get_data: function(frm) {
		if(!frm.doc.__islocal){
			frappe.call({
				doc: frm.doc,
				method: "get_bag",
				callback: function(r) {
					frm.reload_doc()
				}
			});
		}else{
			frappe.msgprint("Please Save Doc First.")
		}
	}
});

var tarnsfer_entry = function (frm) {
	frappe.call({
		doc: frm.doc,
		method: "transfer_entry",
		callback: function(r) {
			if (r.message){
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		}
	});
}
