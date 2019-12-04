// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Packing', {
	loose_stock: function(frm) {
		debugger;
		if( frm.doc.loose_stock && frm.doc.stack_size) {
			cur_frm.set_value("total", parseInt(frm.doc.loose_stock) * parseInt(frm.doc.stack_size));
			refresh_field("total");
		}
	}
})
frappe.ui.form.on('PNI Packing Item', {
	packing: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		if( row.packing_size && row.nos && frm.doc.stack_size) {
			frappe.model.set_value(cdt, cdn,"total", parseInt(row.packing_size) * parseInt(row.nos) * parseInt(frm.doc.stack_size));
			refresh_field("items");
		}
	},
	packing_size: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		if( row.packing_size && row.nos && frm.doc.stack_size) {
			frappe.model.set_value(cdt, cdn,"total", parseInt(row.packing_size) * parseInt(row.nos) * parseInt(frm.doc.stack_size));
			refresh_field("items");
		}
	},
	nos: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		if( row.packing_size && row.nos && frm.doc.stack_size) {
			frappe.model.set_value(cdt, cdn,"total", parseInt(row.packing_size) * parseInt(row.nos) * parseInt(frm.doc.stack_size));
			refresh_field("items");
		}
	}
});
