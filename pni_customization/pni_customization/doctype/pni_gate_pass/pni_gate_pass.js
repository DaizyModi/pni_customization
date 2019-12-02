// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Gate Pass', {
	on_load: function(frm) {
		// frappe.db.get_value('Employee', filters={'user_id':frappe.session.user}, fieldname = ['name'],(r) => {
		// 	debugger;
		// 	frm.set_value("price_list",r.selling_price_list);
		// 	frm.refresh_field("price_list");
		// } )
	}
});
