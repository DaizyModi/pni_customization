// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Sales Order', {
	refresh: function(frm) {
		cur_frm.add_custom_button(__('Sales Order'),
			cur_frm.cscript['Make Sales Order'], __('Create'));
	},
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Sales Order': 'Make Sales Order'
		}
	},
	onload: function(frm) {
		if(!frm.doc.date){
			frm.set_value("date", moment(frappe.datetime.now_datetime()));
		}
		if(!frm.doc.delivery_date){
			frm.set_value("delivery_date", moment(frappe.datetime.now_datetime()));
		}
		if(!frm.doc.user){
			frm.set_value("user",frappe.session.user);
		}
		cur_frm.set_query("price_list", function() {
			return { filters: { selling: 1 } };
		});
		frappe.db.get_value('Selling Settings', 'Selling Settings', 'selling_price_list',(r) => {
			frm.set_value("price_list",r.selling_price_list);
			frm.refresh_field("price_list");
		} )
	},
	user: function(frm) {
		cur_frm.set_query("sales_person", function() {
			return {
				"filters": {
					"pni_user": frm.doc.user,
				}
			};
		});
		
		frappe.db.get_value('Sales Person', {'pni_user':frappe.session.user} , ['name'],(r) => {
			frm.set_value("sales_person",r.name);
		})
		
	}
});

cur_frm.cscript['Make Sales Order'] = function() {
	frappe.model.open_mapped_doc({
		method: "pni_customization.pni_customization.doctype.pni_sales_order.pni_sales_order.make_sales_order",
		frm: cur_frm
	})
}
