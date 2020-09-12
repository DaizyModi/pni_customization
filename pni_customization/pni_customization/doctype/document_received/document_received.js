// Copyright (c) 2020, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Document Received', {
	onload: function(frm) {
		frm.set_query('pni_gate_entry', function(doc) {
			return {
				filters: {
					entry_status: ['not in', ['Delivered']]
				}
			};
		});
	},
});
