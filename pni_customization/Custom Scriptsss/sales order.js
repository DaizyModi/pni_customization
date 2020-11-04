frappe.ui.form.on("Sales Order Item",{
	"item_code" : function (frm, cdt, cdn){
//		cur_frm.clear_table("last_sales_table");
//		cur_frm.clear_table("last_customer_sales_table");
		var d2 = locals[cdt][cdn];
		if(frm.doc.customer && d2.item_code){
			frappe.call({
				"method": "last_records.last_records.doctype.last_purchase_table.last_purchase_table.getLastSalesprice",
				args: {
					item_code: d2.item_code,
				},
				callback:function(r){
					var len=r.message.length;
					for (var i=0;i<len;i++){  
						var row = frm.add_child("last_customer_sales_table");
						row.invoice_number = r.message[i][0];
						row.customer_name = r.message[i][1];
						row.invoice_date = r.message[i][2];
						row.item_code = r.message[i][3];
						row.qty = r.message[i][4];
						row.rate = r.message[i][5];
					}
				}
			});
		}
		if(d2.item_code){
			frappe.call({
				"method": "last_records.last_records.doctype.last_purchase_table.last_purchase_table.getLastSalespriceCustomer",
				args: {
					item_code: d2.item_code,
					customer : frm.doc.customer
				},
				callback:function(r){
					var len=r.message.length;
					for (var i=0;i<len;i++){  
						var row = frm.add_child("last_sales_table");
							row.invoice_number = r.message[i][0];
							row.invoice_date = r.message[i][1];
							row.item_code = r.message[i][2];
							row.qty = r.message[i][3];
							row.rate = r.message[i][4];
					}
				}
			});
		}
		if(d2.price_list_rate>0){
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	);
			frm.refresh_field("items");
		}
	},
	"is_paper_plate": function(frm, cdt, cdn) {
		var d2 = locals[cdt][cdn];
		if(d2.price_list_rate>0){
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	);
			frm.refresh_field("items");
		}
	},
	"paper_cup": function(frm, cdt, cdn) {
		var d2 = locals[cdt][cdn];
		if(d2.price_list_rate>0){
			d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	);
			frm.refresh_field("items");
		}
	},
	"base_uom_rate": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		
		if(parseFloat(d2.base_uom_rate * d2.conversion_factor).toFixed(4) < d2.price_list_rate && d2.price_list_rate > 0){
			frappe.msgprint("[Warning] Rate is less then "+parseFloat(d2.price_list_rate / d2.conversion_factor	));
		}
		
		d2.rate = parseFloat(d2.base_uom_rate * d2.conversion_factor).toFixed(4);
		frm.refresh_field("items");
	},
	"rate": function(frm, cdt, cdn){
		var d2 = locals[cdt][cdn];
		if(d2.rate < d2.price_list_rate && d2.price_list_rate > 0){
			frappe.msgprint("[Warning] Rate is less then "+d2.price_list_rate);
			// d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
		}
	}
});

frappe.ui.form.on('Sales Order', {
	is_order_approved_by_customer(frm) {
	    if(frm.doc.is_order_approved_by_customer === 1){
	        frm.set_value("image","");
	        frm.set_df_property('image','reqd', 1);
	    }
	    if(frm.doc.is_order_approved_by_customer === 0){
	        frm.set_value("image","");
	        frm.set_df_property('image','reqd', 0);
		}
		
	}
});

function showPosition(position){
	frm.set_value("latitude",position.coords.latitude);
	frm.set_value("longitude",position.coords.longitude);
}
       	
frappe.ui.form.on('Sales Order', {
	onload(frm) {
	    if(frm.doc.docstatus === 0){
			navigator.geolocation.getCurrentPosition(showPosition);
			
		}
	},
	refresh(frm){

		setTimeout(() => {
			$("[data-label='Update%20Items'").prop('disabled', true);
			$("[data-label='Status'").find("button").hide();

			if(frappe.user.has_role('System Manager') ){
				$("[data-label='Update%20Items'").prop('disabled', false);
			}
	
			if(frappe.user.has_role('Close Botton Role') ){
				$("[data-label='Status'").find("button").show();
			}
		});

		frm.doc.items.forEach(function(element) {
			if(element.price_list_rate>element.rate && element.price_list_rate > 0 && !element.approve_law_rate__){
				frappe.msgprint("[Warning] Item "+element.item_code +"'s rate is lower then Item Price List");
			}
		});
	}
});


frappe.ui.form.on("Sales Order", "google_map", function(frm) {
   window.open("http://www.google.com/maps/place/" + frm.doc.latitude + "," + frm.doc.longitude);
});

frappe.ui.form.on('Sales Order Item', {
	refresh(frm) {
		cur_frm.fields_dict.child_table_name.grid.toggle_reqd
    ("bottom_size", item_group=="Paper Cup Machine");
	}
});
frappe.ui.form.on('Sales Order',  {
    validate: function(frm) {
        $.each(frm.doc.sales_team,  function(i,  d) {
            frm.set_value("sales_person_name",d.sales_person);
        });
            cur_frm.refresh();
    } 
});
