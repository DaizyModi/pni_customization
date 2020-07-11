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
	}
});