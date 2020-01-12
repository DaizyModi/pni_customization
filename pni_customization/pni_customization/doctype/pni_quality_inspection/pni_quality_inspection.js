// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Quality Inspection', {
	onload: function(frm) {
		if(!frm.doc.inspected_by){
			cur_frm.set_value("inspected_by", frappe.session.user)
		}
	},
	reference_name: function(frm) {
		if(frm.doc.reference_type == "Job Card"){
			frappe.db.get_value("Job Card", frm.doc.reference_name, "employee", (data) => {
				cur_frm.set_value("created_by", data.employee) 
			})
		}
	}
});
