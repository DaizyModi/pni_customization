// Copyright (c) 2020, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Brand Pricing Update Tool', {
	refresh: function(frm) {
		if(!frm.doc.brand_group){
			frm.doc.brand_pricing_table = ""
			refresh_field("brand_pricing_table");
		}

	},
	brand_group: function(frm) {
		if(!frm.doc.brand_group){
			frm.doc.brand_pricing_table = ""
			refresh_field("brand_pricing_table");
			return
		}
		frappe.call({
			"method": "get_brand_list",
			doc: cur_frm.doc,
			callback: function (r) {
				if(r.message){
					frm.doc.brand_pricing_table = ""
					r.message.forEach(function(element) {
						var c = frm.add_child("brand_pricing_table");
						c.brand = element.brand;
					});
					refresh_field("brand_pricing_table");

					frappe.call({
						"method": "get_brand_rate",
						doc: cur_frm.doc,
						callback: function (r) {
							if(r.message){
			
								frm.doc.brand_pricing_table.forEach(function(element) {
									console.log(r.message);
									console.log(element);
									frappe.model.set_value(element.doctype, element.name , "selling_rate", r.message[element.brand])
									debugger;

								})
								refresh_field("brand_pricing_table");
							}	
						}
					})
				}	
			}
		})
	}
});
