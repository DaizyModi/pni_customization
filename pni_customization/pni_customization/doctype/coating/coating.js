// Copyright (c) 2020, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Coating', {
	refresh: function(frm) {
		if(!frm.doc.__islocal && frm.doc.status == 'Pending For Stock Entry'){
			var finish_btn = frm.add_custom_button(__('Create Manufacture Entry'), function(){
				process_production(frm);
			});
			finish_btn.addClass('btn-primary')
		}
	}
});

var process_production = function (frm) {
	frappe.call({
		doc: frm.doc,
		method: "manufacture_entry",
		args:{
			"status": status
		},
		callback: function(r) {
			if (r.message){
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		}
	});
}
