// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Production Plan', {
	refresh: function(frm) {
		if(frm.doc.docstatus==1){
			cur_frm.add_custom_button(__('Paper Cup Job Order'),
				cur_frm.cscript['Make Paper Cup Job Order'], __('Create'));
		}
	},
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Paper Cup Job Order': 'Make Paper Cup Job Order'
		}
	},
	onload: function(frm) {
		if(!frm.doc.date){
			frm.set_value("time", moment(frappe.datetime.now_datetime()).format("HH:mm:ss"));
		}
		if(!frm.doc.user){
			frm.set_value("created_by",frappe.session.user);
		}
	},
	get_pni_so: function(frm) {
		frappe.call({
			doc: frm.doc,
			method: "get_pni_so",
			callback: function(r) {
				refresh_field("production_so");
			}
		});
	},
	get_item_for_manufacture: function(frm) {
		frappe.call({
			doc: frm.doc,
			method: "get_pni_item",
			callback: function(r) {
				refresh_field("pni_production_plan_item");
			}
		});
	}
});

cur_frm.cscript['Make Paper Cup Job Order'] = function() {
	frappe.model.open_mapped_doc({
		method: "pni_customization.pni_customization.doctype.pni_production_plan.pni_production_plan.make_joborder",
		frm: cur_frm
	})
}
