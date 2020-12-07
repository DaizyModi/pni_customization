frappe.ui.form.on('Job Offer', {
	refresh: function(frm) {
		if(!frm.doc.__islocal){
			cur_frm.add_custom_button(__("Employee Onboarding"), function() {
				frappe.model.open_mapped_doc({
					method: "pni_customization.utility.job_offer_utility.open_employee_onboarding",
					frm: cur_frm
				})
			}).addClass('btn-primary')
		}
	}
});