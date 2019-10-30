frappe.ui.form.on('Sales Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog()
	}
});

cur_frm.cscript.add_item_dialog = function(frm) {
	cur_frm.add_custom_button(__("Add Item by Attribute"), function() {
		frappe.prompt(
			[
				{'fieldname': 'item_varient', 'fieldtype': 'Link', 'options': 'Item', 'label': 'Item',
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
				frappe.call({
					method: "pni_customization.utils.get_item_data",
					args: { 
						item: values.item
					},
					callback: (response) => {
						var data;
						data = [{'fieldname': 'item', 'fieldtype': 'Link', 'options': 'Item', 'label': 'Item', 'default': response.message.item , 'read_only':1 }]
						var attr;
						for( attr in response.message.attribute ){
							debugger;
							data.push({'fieldname': response.message.attribute[attr].attribute, 'fieldtype': 'Data', 'label': response.message.attribute[attr].attribute})
						}
						frappe.prompt(
							data,
							function(values){
								show_alert(values.color, 5);
							},
							'Item Varient Selection',
							'Add Item'
						)
					}
				});
			},
			'Item Varient Selection',
			'Add Item'
		)
	}); 
}
