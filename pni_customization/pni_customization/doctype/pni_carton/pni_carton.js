// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Carton', {
	refresh: function(frm) {

	},
	onload: function(frm) {
		if(frm.doc.status == "Delivered"){
			cur_frm.set_df_property("status", "read_only", 1);
		}
	}
});
