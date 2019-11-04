frappe.ui.form.on('Sales Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog()	
	}
});

cur_frm.cscript.add_item_dialog = function(frm) {
	cur_frm.add_custom_button(__("Add Item by Attribute"), function() {
		prompt_for_item_template(frm, "items", "Item Varient Selection", true, function (values) {
			get_attribute_values(frm, "items", "Add Attribute Values", values, function(values, item){
				prompt_attribute_values(frm, "items", "Add Attribute Values", values, item, function(values, item) {
					frappe.call({
						method: "pni_customization.utils.get_item",
						args: { 
							values: values,
							item: item
						},
						callback: (response) => {
							show_alert('This Item Found ' + response.message, 5);
							var d = frappe.model.add_child(cur_frm.doc, "Sales Order Item", "items");
							d.item_code = response.message;
							d.qty = 1;
							frappe.model.set_value(d.doctype, d.idx, "item_code", response.message);
							refresh_field("items");
						}
					})
				})
			})
		});
	}).addClass('btn-primary');
}
var prompt_for_item_template = function(frm, table, title, qty_required, callback) {
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

var get_attribute_values = function(frm, table, title, Rdata, callback_for_get_prompt) {
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

var prompt_attribute_values = function(frm, table, title, response, item, callback) {
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