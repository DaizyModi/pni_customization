frappe.ui.form.on('Material Request', {
	refresh(frm) {
	    if(frm.doc.status != 'Stopped'){
		    frm.add_custom_button(__('Stop'),
					() => frm.events.update_status(frm, 'Stopped'));
		}
	},
	setup: function(frm) {
		debugger;
		frm.set_query("item_code","items", function() {
			return {
				filters: {
					workflow_state: ["in", ["Checked","Approved","Old Item"]]
				}
			}
		});
	},
	onload: function(doc, cdt, cdn) {
		this.frm.set_query("item_code", "items", function() {
			if (doc.material_request_type == "Customer Provided") {
				return{
					query: "erpnext.controllers.queries.item_query",
					filters:{ 'customer': me.frm.doc.customer, workflow_state: ["in", ["Checked","Approved","Old Item"]] }
				}
			} else if (doc.material_request_type != "Manufacture") {
				return{
					query: "erpnext.controllers.queries.item_query",
					filters: {'is_purchase_item': 1, workflow_state: ["in", ["Checked","Approved","Old Item"]]}
				}
			}
		});
	},
});
