frappe.ui.form.on(cur_frm.doctype, {
    "refresh": frm => {
            if (frm.doc.workflow_state && frm.doc.workflow_state == "Pending For Material Issue" && !frm.doc.release_date){
			    frm.set_value("release_date", frappe.datetime.nowdate());
			    frm.save("Update");
            }
            if (frm.doc.workflow_state && frm.doc.workflow_state == "Approved" && frm.doc.release_date){
			    frm.set_value("release_date", "");
			    frm.save("Update");
            }
            if (frm.doc.docstatus === 1) {
		        if (frm.doc.status != 'Stopped' && frm.doc.status != 'Completed') {
				    frm.add_custom_button(__('Short Closed'), function() {
						frappe.call({
							method: "pni_customization.utility.work_order_utility.short_closed",
							args: {
								work_order: frm.doc.name
							},
							callback: function(r) {
								if(r.message && !r.exc) {
									frappe.msgprint("Work Order Short Closed.")
									erpnext.work_order.stop_work_order(frm, "Stopped");
								}
							}
						})
						
				    }, __("Status"));
				}
				if (frm.doc.status == 'Completed') {
				    frm.add_custom_button(__('Short Closed'), function() {
						frappe.call({
							method: "pni_customization.utility.work_order_utility.short_closed_after_complete",
							args: {
								work_order: frm.doc.name
							},
							callback: function(r) {
								if(r.message && !r.exc) {
									frappe.msgprint("Work Order Short Closed.")
									frm.reload_doc()
								}
							}
						})
						
				    }, __("Status"));
			    }
            }
        }
    }
)
frappe.ui.form.on('Work Order', {
	refresh(frm) {
		frm.add_custom_button('Open Quality Inspection', function(){
		    frappe.set_route("List", "PNI Quality Inspection",  {"reference_name": frm.doc.name});
		})
		frm.add_custom_button('Check Include Item In Manufacturing', function(){
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