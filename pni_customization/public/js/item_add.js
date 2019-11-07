frappe.ui.form.on('Sales Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Sales Order Item", "items");
		// var df1 = frappe.meta.get_docfield("Sales Order Item","qty_in_carton", cur_frm.doc.name);
		// df1.read_only = 1;	
		// refresh_field("items");
	}
});

frappe.ui.form.on('Sales Order Item', {
	item_code: function(frm, cdt, cdn) {
		// var row = locals[cdt][cdn]
		// var df1 = frappe.meta.get_docfield("Sales Order Item","qty_in_carton", cdn);
		// if(row.item_group == "Paper Cups"){
		// 	df1.read_only = 0;
		// }else {
		// 	df1.read_only = 1;
		// }
		// debugger;
		// refresh_field("items");
		// debugger;
		// grid_row = frm.get_field("qty_in_carton").grid.get_row(cdn); 
		// grid_row.toggle_editable("qty_in_carton", false);
	},
	qty_in_carton: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn]
		frappe.call({
			method: 'frappe.client.get_value',
			args: {
				'doctype': 'UOM Conversion Detail',
				'fieldname': ["conversion_factor"],
				'parent': 'Item',
			filters: {
				parent: row.item_code,
				uom: 'Carton'
				}
			},
			async: false,
			callback: function(r) {
				if(r.message.conversion_factor > 0){
					frappe.model.set_value(cdt, cdn, "qty", parseFloat(r.message.conversion_factor) * parseFloat(row.qty_in_carton))
				}
			}
		});
	}
});

frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Sales Invoice Item", "items")	
	}
});

frappe.ui.form.on('Purchase Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Purchase Order Item", "items")	
	}
});

frappe.ui.form.on('Purchase Invoice', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Purchase Invoice Item", "items")	
	}
});

frappe.ui.form.on('Work Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Work Order Item", "required_items")	
	}
});

frappe.ui.form.on('BOM', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("BOM Item", "items")	
	}
});

frappe.ui.form.on('Process Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Process Order Item", "materials")	
	}
});

cur_frm.cscript.add_item_dialog = function(item_table_doctype, item_table_fieldname) {
	cur_frm.add_custom_button(__("Add Item by Attribute"), function() {
		prompt_for_item_template("items", "Item Varient Selection", true, function (values) {
			get_attribute_values("items", "Add Attribute Values", values, function(values, item){
				prompt_attribute_values("items", "Add Attribute Values", values, item, function(values, item) {
					frappe.call({
						method: "pni_customization.utils.get_item",
						args: { 
							values: values,
							item: item
						},
						callback: (response) => {
							show_alert('This Item Found ' + response.message.name, 5);
							var d = frappe.model.add_child(cur_frm.doc, item_table_doctype, item_table_fieldname);
							d.item_code = response.message.name;
							d.qty = 1;
							d.delivery_date = cur_frm.doc.delivery_date;
							d.item_name = response.message.item_name;
							d.description = response.message.description;
							d.uom = response.message.stock_uom;
							debugger;
							refresh_field(item_table_fieldname);
						}
					})
				})
			})
		});
	}).addClass('btn-primary');
}
var prompt_for_item_template = function(table, title, qty_required, callback) {
	frappe.prompt(
		[
			{
				'fieldname': 'item_varient', 
				'fieldtype': 'Link', 
				'options': 'Item', 
				'label': 'Item',
				get_query: () => {		
					return {
						filters: {
							has_variants: true
						}
					};
				},
			},
		],
		function(values){
			callback(values);
		},
		__(title),
		__('Add Item')
	)
}

var get_attribute_values = function(table, title, Rdata, callback_for_get_prompt) {
	frappe.call({
		method: "pni_customization.utils.get_item_data",
		args: { 
			item: Rdata.item_varient
		},
		callback: (response) => {
			callback_for_get_prompt(response, Rdata.item_varient);
		}
	});
}

var prompt_attribute_values = function(table, title, response, item, callback) {
	var data = [];
	$.each(response.message.attribute_data || [], function(i, row) {
		if( row.numeric_values == false) {
			data.push(
				{
					'fieldname': i, 
					'fieldtype': 'Select', 
					'label': i,
					'options' : row.values
				}
			)
		} else {
			data.push(
				{
					'fieldname': i, 
					'fieldtype': 'Float', 
					'label': i,
				}
			)
		}
	})
	frappe.prompt(
		data,
		function(values){
			callback(values, item);
		},
		'Item Varient Selection For ' + response.message.item,
		'Add Item'
	)	
}