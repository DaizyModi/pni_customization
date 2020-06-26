frappe.ui.form.on('Delivery Note', {
	scan_carton: function(frm) {
		let scan_barcode_field = frm.fields_dict["scan_carton"];
		fetch_packing(frm, scan_barcode_field, "PNI Carton");
		scan_barcode_field.set_value('');
		refresh_field('scan_carton')
		return false;
	},
	scan_bag: function(frm) {
		let scan_barcode_field = frm.fields_dict["scan_bag"];
		fetch_packing(frm, scan_barcode_field, "PNI Bag");
		scan_barcode_field.set_value('');
		refresh_field('scan_bag')
		return false;
	},
	scan_reel: function(frm) {
		let scan_barcode_field = frm.fields_dict["scan_reel"];
		fetch_packing(frm, scan_barcode_field, "Reel");
		scan_barcode_field.set_value('');
		refresh_field('scan_reel')
		return false;
	},
	item_filter: function(frm) {
		cur_frm.set_query("pni_carton", "pni_packing_table", function(doc, cdt, cdn) {
			let row = locals[cdt][cdn]
			return {
				"filters": {
					"item": doc.item_filter
				}
			}
		})
	},
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
				'default': 'FG Blank and Bottom'
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
					child_doc = frappe.model.add_child(frm.doc, "PNI Packing Table", 'pni_packing_table');
					child_doc.packing_type = "PNI Bag"
					child_doc.pni_carton = entry.name
					child_doc.item = entry.item
					child_doc.total_qty = entry.weight
				});
				refresh_field('pni_packing_table');
				//add_packing_to_item(frm);
			})			
		},
		'Add PNI Bag',
		'Add'
		)
	}
})
frappe.ui.form.on('PNI Packing Table', {
	pni_carton: function(frm, cdt, cdn){
		add_packing_to_item(frm);
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
			
			refresh_field('pni_packing_table')
			add_packing_to_item(frm);
			
		});
	}
}


var add_packing_to_item = function(frm, clear_table = true){
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
	if(clear_table){
		cur_frm.clear_table("items");
	}
	refresh_field("items")
	
	items.forEach(function(value){
		console.log(list_item);
		console.log(value);
		var child = frappe.model.add_child(frm.doc, "Delivery Note Item", "items");
		child.item_code = value
		child.item_name = item_name[value]
		child.description = item_detail[value]
		child.stock_uom = "Nos"
		child.qty = list_item[value]
		child.uom = "Nos"
		child.rate = update_rate(frm, value)
		refresh_field("items")
	})
}

var update_rate = function(frm, item){
	var rate = 0
	if(frm.doc.pni_sales_order_item){
		frm.doc.pni_sales_order_item.forEach(function(value){
			if(value.item == item){
				rate = parseFloat(value.rate);
			}
		})
	}
	return rate;
}