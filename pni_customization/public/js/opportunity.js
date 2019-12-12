frappe.ui.form.on('Opportunity', {
	refresh: function(frm) {
		cur_frm.add_custom_button(__('PNI Sales Order'),
			cur_frm.cscript['Make PNI Sales Order'], __('Create'));
		cur_frm.add_custom_button(__('PNI Quotation'),
				cur_frm.cscript['Make PNI Quotation'], __('Create'));
	}
})
cur_frm.cscript['Make PNI Sales Order'] = function() {
	frappe.model.open_mapped_doc({
		method: "pni_customization.pni_customization.doctype.pni_sales_order.pni_sales_order.make_pni_sales_order_from_opportunity",
		frm: cur_frm
	})
}

cur_frm.cscript['Make PNI Quotation'] = function() {
	frappe.model.open_mapped_doc({
		method: "pni_customization.utils.make_pni_quotation_from_opportunity",
		frm: cur_frm
	})
}