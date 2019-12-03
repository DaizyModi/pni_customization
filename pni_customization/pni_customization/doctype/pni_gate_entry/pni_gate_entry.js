// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Gate Entry', {
	refresh: function(frm) {
		if(!frm.doc.created_by){
			debugger;
			cur_frm.set_value("created_by",frappe.session.user);
		}	
	}
});
