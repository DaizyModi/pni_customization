frappe.ui.form.on('Delivery Note', {
	add_item_pni: function(frm) {

		var list_item = {} 
		var item_name = {}
		var item_detail = {}

		
		
		frm.doc.pni_packing_table.forEach(function(value){
			if(list_item[value.item] == undefined){
				list_item[value.item] = 0;
			}
			list_item[value.item] += value.total_qty;
			item_name[value.item] = value.item_name
			item_detail[value.item] = value.item_description
		})
		
		cur_frm.clear_table("items");
		refresh_field("items")

		frm.doc.pni_delivery_note.forEach(function(value){
			if(list_item[value.item] != undefined){
				var child = frappe.model.add_child(frm.doc, "Delivery Note Item", "items");
				child.item_code = value.item
				child.item_name = item_name[value.item]
				child.description = item_detail[value.item]
				child.stock_uom = "Nos"
				child.qty = list_item[value.item]
				child.uom = "Nos"
				child.rate = value.rate
				refresh_field("items")
			}
		})
	},
	scan_carton: function(frm) {
		let scan_barcode_field = frm.fields_dict["scan_carton"];

		let show_description = function(idx, exist = null) {
			if (exist) {
				scan_barcode_field.set_new_description(__('Row #{0}: Qty increased by 1', [idx]));
			} else {
				scan_barcode_field.set_new_description(__('Row #{0}: Item added', [idx]));
			}
		}

		if(frm.doc.scan_carton) {
			let items_det = "";
			if(frm.doc.pni_delivery_note){
				frm.doc.pni_delivery_note.forEach(function(data){
					items_det += data.item + ",";
				})
			}
			frappe.call({
				method: "pni_customization.utils.get_carton",
				args: { carton: frm.doc.scan_carton, items: items_det }
			}).then(r => {
				const data = r && r.message;

				if (!data || Object.keys(data).length === 0) {
					scan_barcode_field.set_new_description(__('Cannot find Item with this barcode'));
					return;
				}

				let cur_grid = frm.fields_dict.pni_packing_table.grid;

				let row_to_modify = null;
								
				row_to_modify = frappe.model.add_child(frm.doc, cur_grid.doctype, 'pni_packing_table');
				

				show_description(row_to_modify.idx, row_to_modify.pni_carton);

				frm.from_barcode = true;
				frappe.model.set_value(row_to_modify.doctype, row_to_modify.name, {
					pni_carton: data.name,
				});
				frappe.model.set_value(row_to_modify.doctype,row_to_modify.name, "total_qty", data['total']);
				['item', 'item_name', 'item_description', ''].forEach(field => {
					if (data[field] && frappe.meta.has_field(row_to_modify.doctype, field)) {
						frappe.model.set_value(row_to_modify.doctype,
							row_to_modify.name, field, data[field]);
					}
				});

				scan_barcode_field.set_value('');
				refresh_field('scan_carton')
				refresh_field('pni_packing_table')
				
				// add item to table
				var list_item = {} 
				var item_name = {}
				var item_detail = {}

				
				
				frm.doc.pni_packing_table.forEach(function(value){
					if(list_item[value.item] == undefined){
						list_item[value.item] = 0;
					}
					list_item[value.item] += value.total_qty;
					item_name[value.item] = value.item_name
					item_detail[value.item] = value.item_description
				})
				
				if(!frm.doc.paper_plate){
					cur_frm.clear_table("items");
					refresh_field("items")
					frm.doc.pni_delivery_note.forEach(function(value){
						if(list_item[value.item] != undefined){
							var child = frappe.model.add_child(frm.doc, "Delivery Note Item", "items");
							child.item_code = value.item
							child.item_name = item_name[value.item]
							child.description = item_detail[value.item]
							child.stock_uom = "Nos"
							child.qty = list_item[value.item]
							child.uom = "Nos"
							child.rate = value.rate
							refresh_field("items")
						}
					})
				}
			});
		}
		return false;
	},
	// pni_delivery_note: function (frm) {
	// 	let temp = []
	// 	if(cur_frm.doc.pni_delivery_note){
	// 		debugger;
	// 		for(intem in cur_frm.doc.pni_delivery_note){
	// 			temp.push(cur_frm.doc.pni_delivery_note[intem].item);
	// 		}
	// 	}
	// 	debugger;
	// 	frm.set_query("pni_carton", function () {
	// 		return {
	// 			filters: [
	// 				["PNI Carton","item","in",temp]
	// 			]
	// 		}
	// 	});
	// }
})
frappe.ui.form.on('PNI Packing Table', {
	
})