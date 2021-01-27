frappe.ui.form.on('BOM', {
	refresh(frm) {
		frm.add_custom_button(__('Open Setup and Work Instruction Plan'), function(){
		    frappe.set_route("List", "Setup Plan",  {"bom_no": frm.doc.name});
		})
		frm.add_custom_button(__('Check Include Item In Manufacturing'), function(){
		    frappe.call({
				method: "pni_customization.utility.bom_utility.include_item_in_manufacturing",
				args: {
					bom: frm.doc.name
				},
				callback: function(r) {
					if(r.message && !r.exc) {
						frappe.msgprint("BOM Updated For Include Item In Manufacturing")
						frm.reload_doc()
					}
				}
			})
		})
		frm.add_custom_button(__('Update Item Name'), function(){
		    frappe.call({
				method: "pni_customization.utility.bom_utility.update_item_name",
				args: {
					bom: frm.doc.name
				},
				callback: function(r) {
					if(r.message && !r.exc) {
						frappe.msgprint("BOM Item Name Updated.")
						frm.reload_doc()
					}
				}
			})
		})
	}
})