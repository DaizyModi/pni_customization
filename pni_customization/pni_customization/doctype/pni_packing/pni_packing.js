// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Packing', {
	loose_stock: function(frm) {
		// if( frm.doc.loose_stock && frm.doc.stack_size) {
		// 	cur_frm.set_value("total", parseInt(frm.doc.loose_stock) * parseInt(frm.doc.stack_size));
		// 	refresh_field("total");
		// }
	},
	select_employee_group: function(frm) {
		frappe.call({
			"method": "get_employee_list",
			doc: cur_frm.doc,
			callback: function (r) {
				if(r.message){

					r.message.forEach(function(element) {
						var c = frm.add_child("employee");
						c.duty = element.duty;
						c.employee = element.employee;
					});
					refresh_field("employee");
				}	
			}
		})
	},
	refresh_carton_data: function(frm) {
		// if( frm.doc.carton_data.length == 0 ) {
		// 	frm.doc.items.forEach(function(value){
		// 		console.log(value);
		// 		for(let i =0; i< value.nos; i++){
		// 			var child = frappe.model.add_child(frm.doc, "PNI Packing Carton", "carton_data");
		// 			child.pni_packing_type = value.packing
		// 			child.packing_size = value.packing_size
		// 			refresh_field("carton_data")
		// 		}
		// 	});
		// } else {
		// 	frappe.msgprint("Please Delete Data in Carton Data Table or Add Manual data in that table");
		// }
	},
	enter_carton_weight: function(frm){
		// $.each(frm.doc.carton_data || [], function(i, v) {
		// 	frappe.prompt([
		// 		{
		// 			'label': 'Carton',
		// 			'fieldname': 'carton_id', 
		// 			'fieldtype': 'Link', 
		// 			'options': 'PNI Carton', 
		// 			'read_only': true, 
		// 			'default': v.carton_id
		// 		},
		// 		{
		// 			'label': 'Weight in KG',
		// 			'fieldname': 'weight', 
		// 			'fieldtype': 'Float',
		// 			'default': v.weight
		// 		},
		// 		{
		// 			'fieldname': 'id', 
		// 			'fieldtype': 'Data',
		// 			'hidden': true,
		// 			'default': v.name
		// 		},
		// 		{
		// 			'fieldname': 'doctype', 
		// 			'fieldtype': 'Data',
		// 			'hidden': true,
		// 			'default': v.doctype
		// 		},

		// 	],
		// 	function(values){
		// 		frappe.model.set_value(values.doctype, values.id, "weight", values.weight);
		// 		refresh_field("carton_data")
		// 	},
		// 	'Add Weight of Carton',
		// 	'Add'
		// 	)
		// })
	}
})
// frappe.ui.form.on('PNI Packing Item', {
// 	// packing: function(frm, cdt, cdn) {
// 	// 	var row = locals[cdt][cdn]
// 	// 	if( row.packing_size && row.nos && frm.doc.stack_size) {
// 	// 		frappe.model.set_value(cdt, cdn,"total", parseInt(row.packing_size) * parseInt(row.nos) * parseInt(frm.doc.stack_size));
// 	// 		refresh_field("items");
// 	// 	}
// 	// },
// 	// packing_size: function(frm, cdt, cdn) {
// 	// 	var row = locals[cdt][cdn]
// 	// 	if( row.packing_size && row.nos && frm.doc.stack_size) {
// 	// 		frappe.model.set_value(cdt, cdn,"total", parseInt(row.packing_size) * parseInt(row.nos) * parseInt(frm.doc.stack_size));
// 	// 		refresh_field("items");
// 	// 	}
// 	// },
// 	// nos: function(frm, cdt, cdn) {
// 	// 	var row = locals[cdt][cdn]
// 	// 	if( row.packing_size && row.nos && frm.doc.stack_size) {
// 	// 		frappe.model.set_value(cdt, cdn,"total", parseInt(row.packing_size) * parseInt(row.nos) * parseInt(frm.doc.stack_size));
// 	// 		refresh_field("items");
// 	// 	}
// 	// }
// });
