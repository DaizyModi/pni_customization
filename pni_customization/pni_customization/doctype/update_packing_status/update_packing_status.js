// Copyright (c) 2020, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Update Packing Status', {
	// refresh: function(frm) {

	// }
	add_pni_bag: function(frm) {
		frappe.prompt([
			{
				'fieldname': 'item', 
				'fieldtype': 'Link', 
				'label': 'PNI Bag Item', 
				'reqd': 1,
				'options': 'Item'	
			},
			{
				'fieldname': 'qty', 
				'fieldtype': 'Int', 
				'label': 'Qty', 
				'reqd': 1
			},
			{
				'fieldname': 'packing_category',
				'fieldtype': 'Link',
				'label': 'Packing Category',
				'options': 'Packing Category'
			},
			{
				'fieldname': 'warehouse',
				'fieldtype': 'Link',
				'label': 'Warehouse',
				'options': 'Warehouse',
				'default': 'FG Blank and Bottom - PNI'
			},
			{
				'fieldname': 'weight',
				'fieldtype': 'Float',
				'label': 'Weight',
			}  
		],
		function(values){
			frappe.call({
				method: "pni_customization.utils.get_pni_bags",
				args: { 'item': values.item, 'qty':values.qty, 'weight':values.weight, 'packing_category': values.packing_category, 'warehouse': values.warehouse }
			}).then(r => {
				const data = r && r.message;
				console.log(data);
				data.forEach(function(entry) {
					let child_doc = ""
					child_doc = frappe.model.add_child(frm.doc, "Packing Bag Status", 'packing_bag_status');
					child_doc.pni_carton = entry.name
				});
				refresh_field('packing_bag_status');
				//add_packing_to_item(frm);
			})			
		},
		'Add PNI Bag',
		'Add'
		)
	}
});
