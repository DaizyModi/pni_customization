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
		frm.set_query('pni_address', function(doc) {
			if(!doc.pni_reference_type) {
				frappe.throw(__('Please set Reference Type'));
			}

			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: doc.pni_reference_type,
					link_name: doc.pni_reference
				}
			};
		});
	},
	pni_address: function(frm) {
		debugger;
		erpnext.utils.get_address_display(frm, 'pni_address', 'pni_address_display', false);
		debugger;
	}
})