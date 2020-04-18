frappe.ui.form.on('Delivery Note', {
	scan_carton: function(frm) {
		let scan_barcode_field = frm.fields_dict["scan_carton"];
		fetch_packing(frm, scan_barcode_field, "PNI Carton");
		refresh_field('scan_carton')
		return false;
	},
	scan_bag: function(frm) {
		let scan_barcode_field = frm.fields_dict["scan_bag"];
		fetch_packing(frm, scan_barcode_field, "PNI Bag");
		refresh_field('scan_bag')
		return false;
	},
	scan_reel: function(frm) {
		let scan_barcode_field = frm.fields_dict["scan_reel"];
		fetch_packing(frm, scan_barcode_field, "Reel");
		refresh_field('scan_reel')
		return false;
	}
})

var fetch_packing = function(frm, scan_barcode_field, doctype){
	
	let show_description = function(idx, exist = null) {
		if (exist) {
			scan_barcode_field.set_new_description(__('Row #{0}: Qty increased by 1', [idx]));
		} else {
			scan_barcode_field.set_new_description(__('Row #{0}: Item added', [idx]));
		}
	}

	if(scan_barcode_field.value) {
		
		frappe.call({
			method: "pni_customization.utils.get_packing",
			args: { packing: scan_barcode_field.value, doctype:doctype }
		}).then(r => {
			const data = r && r.message;

			if (!data || Object.keys(data).length === 0) {
				scan_barcode_field.set_new_description(__('Cannot find Item with this barcode'));
				return;
			}
			if(frm.doc.pni_packing_table){
				const existing_item_row = frm.doc.pni_packing_table.find(d => d.pni_carton === data.name);
				debugger;
				if(existing_item_row){
					scan_barcode_field.set_new_description(__('Already Added'));
					return;
				}
			}
			let cur_grid = frm.fields_dict.pni_packing_table.grid;

			let row_to_modify = null;
							
			row_to_modify = frappe.model.add_child(frm.doc, cur_grid.doctype, 'pni_packing_table');
			

			show_description(row_to_modify.idx, row_to_modify.pni_carton);

			frm.from_barcode = true;
			
			frappe.model.set_value(row_to_modify.doctype, row_to_modify.name, {
				packing_type: doctype,
			});

			frappe.model.set_value(row_to_modify.doctype, row_to_modify.name, {
				pni_carton: data.name,
			});
			
			if(doctype == "PNI Carton"){
				frappe.model.set_value(row_to_modify.doctype,row_to_modify.name, "total_qty", data['total']);
			} else {
				frappe.model.set_value(row_to_modify.doctype,row_to_modify.name, "total_qty", data['weight']);
			}
			['item', 'item_name', 'item_description', ''].forEach(field => {
				if (data[field] && frappe.meta.has_field(row_to_modify.doctype, field)) {
					frappe.model.set_value(row_to_modify.doctype,
						row_to_modify.name, field, data[field]);
				}
			});

			scan_barcode_field.set_value('');
			
			refresh_field('pni_packing_table')
			
			// add item to table
			var list_item = {} 
			var item_name = {}
			var item_detail = {}
			var items = []
			
			
			frm.doc.pni_packing_table.forEach(function(value){
				if(list_item[value.item] == undefined){
					list_item[value.item] = 0;
				}
				if(!items.includes(value.item)){
					items.push(value.item);
				}
				list_item[value.item] += value.total_qty;
				item_name[value.item] = value.item_name
				item_detail[value.item] = value.item_description
			})
			
			cur_frm.clear_table("items");
			refresh_field("items")
			
			items.forEach(function(value){
				console.log(list_item);
				console.log(value);
				debugger;
				var child = frappe.model.add_child(frm.doc, "Delivery Note Item", "items");
				child.item_code = value
				child.item_name = item_name[value]
				child.description = item_detail[value]
				child.stock_uom = "Nos"
				child.qty = list_item[value]
				child.uom = "Nos"
				// child.rate = value.rate
				refresh_field("items")
			})
		});
	}
}