frappe.ui.form.on('Stock Entry', {
	scrap_entry: function(frm){
		if(frm.doc.scrap_entry){
			frappe.model.set_value(frm.doctype,frm.docname,"stock_entry_type","Material Receipt");
			frappe.model.set_value(frm.doctype,frm.docname,"pni_reference_type","Workstation");
		}
	},
	refresh: function(frm) {
		if(frm.doc.pni_reference_type){
			frm.add_custom_button(__('Open '+frm.doc.pni_reference_type), function(){
				frappe.set_route("List", frm.doc.pni_reference_type.toString());
				//"filter_date": frm.doc.date
			})
		}
	}
})