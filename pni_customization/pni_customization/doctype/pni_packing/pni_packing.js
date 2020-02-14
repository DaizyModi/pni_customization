// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt
$(document).ready(function(){
	$("[data-fieldname='print_carton']").find("a.grey").click(function(event){
		event.preventDefault();
		alert("The paragraph was clicked.");
	});
});
frappe.ui.form.on('PNI Packing', {
	loose_stock: function(frm) {
	
	},
	onload: function(frm) {
		cur_frm.set_query("workstation", function() {
			return { filters: { papercup_forming_machine: 1 } };
		});
	},
	select_employee_group: function(frm) {
		frappe.call({
			"method": "get_employee_list",
			doc: cur_frm.doc,
			callback: function (r) {
				if(r.message){

					r.message.forEach(function(element) {
						var c = frm.add_child("employee");
						c.duty = element.duty;
						c.employee = element.employee;
					});
					refresh_field("employee");
				}	
			}
		})
	},
	refresh_carton_data: function(frm) {

	},
	enter_carton_weight: function(frm){
		
	}
})