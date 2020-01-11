// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Sales Order', {
	refresh: function(frm) {
		cur_frm.add_custom_button(__('Payment Entry'),
			cur_frm.cscript['Make Payment Entry'], __('Create'));
		cur_frm.add_custom_button(__('Delivery Note'),
			cur_frm.cscript['Make Delivery Note'], __('Create'));
	},
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Payment Entry': 'Make Payment Entry',
			'Delivery Note': 'Make Delivery Note'
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
		if(!frm.doc.customer_name){
			// frm.set_value("customer_name",frappe.db.get_value("Customer", frm.doc.customer, "customer_name").responseJSON.message.customer_name);
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
			console.log(r);
			debugger;
			if(typeof r !== 'undefined' && typeof r.name !== 'undefined'){
				frm.set_value("sales_person",r.name);
			}else{
				frappe.msgprint("Sales Person is not created for Employee with user " + frappe.session.user)
			}
		})
		
	}
});

cur_frm.cscript['Make Payment Entry'] = function() {
	frappe.model.open_mapped_doc({
		method: "pni_customization.pni_customization.doctype.pni_sales_order.pni_sales_order.make_payment_entry",
		frm: cur_frm
	})
}

cur_frm.cscript['Make Delivery Note'] = function() {
	frappe.model.open_mapped_doc({
		method: "pni_customization.pni_customization.doctype.pni_sales_order.pni_sales_order.make_delivery_note",
		frm: cur_frm
	})
}

// cur_frm.cscript['Make Sales Order'] = function() {
// 	frappe.model.open_mapped_doc({
// 		method: "pni_customization.pni_customization.doctype.pni_sales_order.pni_sales_order.make_sales_order",
// 		frm: cur_frm
// 	})
// }
