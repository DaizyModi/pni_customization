// Copyright (c) 2021, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Workstation Price Update Tool', {
	refresh: function(frm) {
		if(!frm.doc.department){
			frm.doc.workstation_price = ""
			refresh_field("workstation_price");
		}
	},
	department: function(frm) {
		if(!frm.doc.department){
			frm.doc.workstation_price = ""
			refresh_field("workstation_price");
			return
		}
		frappe.call({
			"method": "get_workstation_list",
			doc: cur_frm.doc,
			callback: function (r) {
				if(r.message){
					debugger;
					frm.doc.workstation_price = ""
					r.message.forEach(function(element) {
						var c = frm.add_child("workstation_price");
						c.workstation = element.name;
						c.pni_rate = element.pni_rate;
					});
					refresh_field("workstation_price");
				}	
			}
		})
	}
});
