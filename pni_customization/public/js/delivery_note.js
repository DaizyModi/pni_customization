frappe.ui.form.on('Delivery Note', {
	"add_item_pni": function(frm) {

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
	}
})
frappe.ui.form.on('PNI Packing Table', {
	pni_carton: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
	}
})