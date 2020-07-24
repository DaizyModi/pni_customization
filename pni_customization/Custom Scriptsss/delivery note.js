frappe.ui.form.on("Delivery Note Item",{
	"item_code" : function (frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		
		if(d2.price_list_rate>0){
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
			frm.refresh_field("items")
		}
	},
	"is_paper_plate": function(frm, cdt, cdn) {
		var d2 = locals[cdt][cdn];
		if(d2.price_list_rate>0){
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
			frm.refresh_field("items")
		}
	},
	"paper_cup": function(frm, cdt, cdn) {
		var d2 = locals[cdt][cdn];
		if(d2.price_list_rate>0){
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
			frm.refresh_field("items")
		}
	},
	"base_uom_rate": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		
		if(parseFloat(d2.base_uom_rate * d2.conversion_factor) < d2.price_list_rate && d2.price_list_rate > 0){
			frappe.msgprint("[Warning] Rate is less then "+parseFloat(d2.price_list_rate / d2.conversion_factor	))
		}
		
		d2.rate = parseFloat(d2.base_uom_rate * d2.conversion_factor)
		frm.refresh_field("items")
	},
	"rate": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		if(d2.rate < d2.price_list_rate && d2.price_list_rate > 0){
			frappe.msgprint("[Warning] Rate is less then "+d2.price_list_rate)
			// d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
		}
	}
});
       	
frappe.ui.form.on('Delivery Note', {
	refresh(frm){
		frm.doc.items.forEach(function(element) {
			if(element.price_list_rate>element.rate && element.price_list_rate > 0 && !element.approve_law_rate__){
				frappe.msgprint("[Warning] Item "+element.item_code +"'s rate is lower then Item Price List");
			}
		})
		if(frm.doc.is_return && frm.doc.__islocal){
			frm.set_value("naming_series","MAT-CRN-.YYYY.-");
		}
		const doc = frm.doc;
		debugger;
		if(doc.payment_terms_template && !doc.payment_schedule.length && frm.doc.__islocal) {
			var posting_date = doc.posting_date || doc.transaction_date;
			frappe.call({
				method: "erpnext.controllers.accounts_controller.get_payment_terms",
				args: {
					terms_template: doc.payment_terms_template,
					posting_date: posting_date,
					grand_total: doc.rounded_total || doc.grand_total,
					bill_date: doc.bill_date
				},
				callback: function(r) {
					if(r.message && !r.exc) {
						frm.set_value("payment_schedule", r.message);
					}
				}
			})
		}
	},
	payment_terms_template: function(frm) {
		debugger;
		const doc = frm.doc;
		if(doc.payment_terms_template ) {
			var posting_date = doc.posting_date || doc.transaction_date;
			frappe.call({
				method: "erpnext.controllers.accounts_controller.get_payment_terms",
				args: {
					terms_template: doc.payment_terms_template,
					posting_date: posting_date,
					grand_total: doc.rounded_total || doc.grand_total,
					bill_date: doc.bill_date
				},
				callback: function(r) {
					if(r.message && !r.exc) {
						frm.set_value("payment_schedule", r.message);
					}
				}
			})
		}
	}
});