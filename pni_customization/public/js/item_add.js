frappe.ui.form.on('Sales Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Sales Order Item", "items");
	},
	customer: function(frm) {
		frm.doc.customer_outstanding = []
		frm.doc.total_customer_outstanding = ""
		if(frm.doc.customer){
			frappe.call({
				method:"pni_customization.utils.get_outstanding_invoice",
				args: {
					customer:frm.doc.customer
				}, 
				callback: function(r) { 
					console.log(r.message);
					r.message.data.forEach(function(element) {
						var c = frm.add_child("customer_outstanding");
						c.sales_invoice = element.name;
						c.date = element.posting_date;
						c.invoice_amt = element.rounded_total;
						c.outstanding_amt = element.outstanding_amount;
					});
					frappe.model.set_value(frm.doctype,frm.docname,"total_customer_outstanding",r.message.total);
					refresh_field("customer_outstanding");
				}
			})
		}
		refresh_field("customer_outstanding");
	}
});

// frappe.ui.form.on('Sales Order Item', {
// });

frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Sales Invoice Item", "items")	
	}
});

frappe.ui.form.on('Purchase Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Purchase Order Item", "items")	
	},
	setup:function (frm) {
		frm.set_query("repair_job_work_transfer_entry", function () {
		    return {
			    filters: {
					purpose: "Send to Warehouse",
					pni_reference: frm.doc.supplier,
					docstatus: 1
			    }
			}
		});
	},
	repair_job_work_transfer_entry: function(frm) {
		if(frm.doc.repair_job_work_transfer_entry){
			frappe.call({
				method:"pni_customization.utility.purchase_order_utility.get_stock_entry_data",
				args: {
					stock_entry:frm.doc.repair_job_work_transfer_entry
				}, 
				callback: function(r) { 
					console.log(r.message);
					frm.doc.stock_entry_data = ""
					r.message.forEach(function(element) {
						var c = frm.add_child("stock_entry_data");
						c.s_warehouse = element.s_warehouse;
						c.t_warehouse = element.t_warehouse;
						c.item_code = element.item_code;
						c.item_group = element.item_group;
						c.qty = element.qty;
					});
					refresh_field("stock_entry_data");
				}
			})
		} else {
			frm.doc.stock_entry_data = ""
			refresh_field("stock_entry_data");
		}
	}
});

frappe.ui.form.on('Purchase Invoice', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Purchase Invoice Item", "items")	
	}
});

frappe.ui.form.on('Work Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Work Order Item", "required_items")	
	}
});

frappe.ui.form.on('BOM', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("BOM Item", "items")
		cur_frm.add_custom_button(__("Update BOM with Default Active"), function() {
			function sleep(ms) {
				return new Promise(resolve => setTimeout(resolve, ms));
			 }
			frappe.call({
				method: "pni_customization.utility.bom_utility.update_bom_default_active",
				args: { 
					bom: frm.doc.name
				},
				callback: (response) => {
					if(response.message){
						var bom = []
						for (var old_bom in response.message){
							
							if(!bom.includes(old_bom)){
								
								let d = new frappe.ui.Dialog({
									title: 'Enter details',
									fields: [
										{
											label: 'Old BOM',
											fieldname: 'current_bom',
											fieldtype: 'Link',
											options: 'BOM',
											read_only: true,
											default: old_bom
										},
										{
											label: 'New BOM',
											fieldname: 'new_bom',
											fieldtype: 'Link',
											options: 'BOM',
											read_only: true,
											default: response.message[old_bom]
										}
									],
									primary_action_label: 'Process',
									primary_action(values) {
										console.log(values);
										frappe.call({
											method: "erpnext.manufacturing.doctype.bom_update_tool.bom_update_tool.enqueue_replace_bom",
											freeze: true,
											args: {
												args: {
													"current_bom": values.current_bom,
													"new_bom": values.new_bom
												}
											}
										});
										d.hide();
									}
								});
								
								d.show();
								// console.log("Bom "+old_bom + " replacement intiated with bom "+response.message[old_bom])
								// frappe.msgprint("Bom "+old_bom + " replacement intiated with bom "+response.message[old_bom])
								// frappe.call({
								// 	method: "erpnext.manufacturing.doctype.bom_update_tool.bom_update_tool.enqueue_replace_bom",
								// 	freeze: true,
								// 	args: {
								// 		args: {
								// 			"current_bom": old_bom,
								// 			"new_bom": response.message[old_bom]
								// 		}
								// 	}
								// });
								// debugger;
								bom.push(old_bom)
								// sleep(300);
								console.log("Afrter Sleep")
							}
						}
						console.log("Bom Enque for Replace")
						frappe.msgprint("Bom Enque for Replace")
					}
				}
			})
		})
		cur_frm.add_custom_button(__("Update BOM with New BOM"), function() {
			frappe.call({
				method: "pni_customization.utility.bom_utility.update_bom_with_new_bom",
				args: { 
					bom: frm.doc.name
				},
				callback: (response) => {
					if(response.message){
						frappe.msgprint(response.message)
					}
				}
			})
		})	
	}
});

frappe.ui.form.on('Process Order', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Process Order Item", "materials")	
	}
});

frappe.ui.form.on('Quotation', {
	refresh: function(frm) {
		cur_frm.cscript.add_item_dialog("Quotation Item", "items")	
	}
});

cur_frm.cscript.add_item_dialog = function(item_table_doctype, item_table_fieldname) {
	cur_frm.add_custom_button(__("Add Item by Attribute"), function() {
		prompt_for_item_template("items", "Item Varient Selection", true, function (values) {
			get_attribute_values("items", "Add Attribute Values", values, function(values, item){
				prompt_attribute_values("items", "Add Attribute Values", values, item, function(values, item) {
					frappe.call({
						method: "pni_customization.utils.get_item",
						args: { 
							values: values,
							item: item
						},
						callback: (response) => {
							show_alert('This Item Found ' + response.message.name, 5);
							var d = frappe.model.add_child(cur_frm.doc, item_table_doctype, item_table_fieldname);
							d.item_code = response.message.name;
							d.qty = 1;
							d.delivery_date = cur_frm.doc.delivery_date;
							d.item_name = response.message.item_name;
							d.description = response.message.description;
							d.uom = response.message.stock_uom;
							debugger;
							refresh_field(item_table_fieldname);
						}
					})
				})
			})
		});
	}).addClass('btn-primary');
}
var prompt_for_item_template = function(table, title, qty_required, callback) {
	frappe.prompt(
		[
			{
				'fieldname': 'item_varient', 
				'fieldtype': 'Link', 
				'options': 'Item', 
				'label': 'Item',
				get_query: () => {		
					return {
						filters: {
							has_variants: true
						}
					};
				},
			},
		],
		function(values){
			callback(values);
		},
		__(title),
		__('Add Item')
	)
}

var get_attribute_values = function(table, title, Rdata, callback_for_get_prompt) {
	frappe.call({
		method: "pni_customization.utils.get_item_data",
		args: { 
			item: Rdata.item_varient
		},
		callback: (response) => {
			callback_for_get_prompt(response, Rdata.item_varient);
		}
	});
}

var prompt_attribute_values = function(table, title, response, item, callback) {
	var data = [];
	$.each(response.message.attribute_data || [], function(i, row) {
		if( row.numeric_values == false) {
			data.push(
				{
					'fieldname': i, 
					'fieldtype': 'Select', 
					'label': i,
					'options' : row.values
				}
			)
		} else {
			data.push(
				{
					'fieldname': i, 
					'fieldtype': 'Float', 
					'label': i,
				}
			)
		}
	})
	frappe.prompt(
		data,
		function(values){
			callback(values, item);
		},
		'Item Varient Selection For ' + response.message.item,
		'Add Item'
	)	
}