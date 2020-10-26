frappe.ui.form.on(cur_frm.doctype, {
    "refresh": frm => {
           if (frm.doc.workflow_state == "Pending For Material Issue" && !frm.doc.release_date){
			   frm.set_value("release_date", frappe.datetime.nowdate());
			   frm.save("Update");
           }
           if (frm.doc.workflow_state == "Approved" && frm.doc.release_date){
			   frm.set_value("release_date", "");
			   frm.save("Update");
           }
     }
})
frappe.ui.form.on('Work Order', {
	refresh(frm) {
		frm.add_custom_button(__('Open Quality Inspection'), function(){
		    frappe.set_route("List", "PNI Quality Inspection",  {"reference_name": frm.doc.name});
		})
		frm.add_custom_button(__('Check Include Item In Manufacturing'), function(){
		    frappe.call({
				method: "pni_customization.utility.work_order_utility.include_item_in_manufacturing",
				args: {
					work_order: frm.doc.name
				},
				callback: function(r) {
					if(r.message && !r.exc) {
						frappe.msgprint("Work Order Updated For Include Item In Manufacturing")
						frm.reload_doc()
					}
				}
			})
		})
		if (frm.doc.docstatus === 1
			&& frm.doc.operations && frm.doc.operations.length
			) {

			const not_completed2 = frm.doc.operations.filter(d => {
				if(d.status != 'Completed') {
					return true;
				}
			});

			if(not_completed2 && not_completed2.length) {
				frm.add_custom_button(__('Create Job Card 2'), () => {
					frm.trigger("make_job_card");
				}).addClass('btn-primary');
			}
		}
	}
})
frappe.ui.form.on('Work Order', {
	refresh(frm) {
		frm.add_custom_button(__('Open Setup and Work Instruction Plan'), function(){
		    frappe.set_route("List", "Setup Plan",  {"bom_no": frm.doc.bom_no});
		})
	}
})