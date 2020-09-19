frappe.ui.form.on('Item', {
	refresh: function(frm) {
		if(frm.doc.pni_material_type!="Machinery"){
			frm.toggle_display("pni_item_code",true)
			frm.toggle_display("naming_series",false)
		}else{
			frm.toggle_display("pni_item_code",false)
			frm.toggle_display("naming_series",true)
		}
		if(!frm.doc.__islocal){
			frm.toggle_display("pni_item_code",false)
		}
	},
	pni_material_type: function(frm){
		if(frm.doc.pni_material_type!="Machinery"){
			frm.toggle_display("pni_item_code",true)
			frm.toggle_display("naming_series",false)
		}else{
			frm.toggle_display("pni_item_code",false)
			frm.toggle_display("naming_series",true)
		}
	}
})