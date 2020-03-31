frappe.ui.form.on('Stock Entry', {
	scrap_entry: function(frm){
		if(frm.doc.scrap_entry){
			frappe.model.set_value(frm.doctype,frm.docname,"stock_entry_type","Material Receipt");
			frappe.model.set_value(frm.doctype,frm.docname,"pni_reference_type","Workstation");
		}
	}
})