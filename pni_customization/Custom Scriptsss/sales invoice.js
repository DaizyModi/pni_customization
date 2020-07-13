frappe.ui.form.on("Sales Invoice Item",{
	"item_code" : function (frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
	},
	"uom": function(frm, cdt,cdn){
		var d2 = locals[cdt][cdn];
		d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
	},
	"qty": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
		frm.refresh_field("items")
	},
	"base_uom_rate": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		if(parseFloat(d2.base_uom_rate * d2.conversion_factor) < d2.price_list_rate){
			frappe.msgprint("Rate can't be less then "+parseFloat(d2.price_list_rate / d2.conversion_factor	))
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
			frm.refresh_field("items")
			return;
		}
		d2.rate = parseFloat(d2.base_uom_rate * d2.conversion_factor)
		frm.refresh_field("items")
	},
	"rate": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		if(d2.rate < d2.price_list_rate){
			frappe.msgprint("Rate can't be less then "+d2.price_list_rate)
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
			frm.refresh_field("items")
		}
	}
});

frappe.ui.form.on('Sales Invoice', {
	refresh(frm){
		if(frm.doc.is_return && frm.doc.__islocal){
			frm.set_value("naming_series","CN-.YYYY.-");
		}
	}
});