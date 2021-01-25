frappe.ui.form.on('Purchase Order', {
	refresh: function(frm) {

		if( cur_frm.doc.workflow_state == "Short Closed" && cur_frm.doc.status!="Closed" && !cur_frm.doc.__islocal && !cur_frm.doc.disable_auto_close){
			status = "Closed"
			frappe.call({
				method: "erpnext.buying.doctype.purchase_order.purchase_order.update_status",
				args: {status: status, name: cur_frm.doc.name},
				callback: function(r) {
					cur_frm.set_value("status", status);
					cur_frm.reload_doc();
				}
			})
		}

		if (frm.doc.workflow_state && cur_frm.doc.workflow_state == 'Rejected'){
			var prompt_already_shown = true;
			var comments = cur_frm.timeline.get_comments();
			var i;
			for (i=0; i < comments.length; i++) {
			    if (comments[i].content.includes("Reason for reject:")) {
			            prompt_already_shown = false;
			    }  
			}
			if (prompt_already_shown) {
				frappe.prompt([
					{'fieldname': 'rejection', 'fieldtype': 'Small Text', 'label': 'Reason', 'reqd': 1}  
					],
					function(values){
						cur_frm.timeline.insert_comment("<b>Reason for reject:</b><br>" + values.rejection);
					},
					'Reason for Rejection',
					'Submit'
				);
			}
		}
		
		frm.add_custom_button(__('Open Quoted Item Comparison'), function(){
		    frappe.set_route("query-report", "Quoted Item Comparison");
		    //"filter_date": frm.doc.date
		})
		frm.add_custom_button(__('Get Item History'), function(){
			cur_frm.clear_table("last_purchase_table");
			cur_frm.clear_table("last_supplier_purchase_table");
			cur_frm.clear_table("quotation_table");
			cur_frm.clear_table("supplier_quotation_table");
			cur_frm.doc.items.forEach(function(data){
				frappe.call({
					"method": "last_records.last_records.doctype.last_purchase_table.last_purchase_table.getLastprice",
					args: {
							item_code: data.item_code,
							supplier: frm.doc.supplier
					},
					callback:function(r){
						var len=r.message.length;
						for (var i=0;i<len;i++){  
							var row = frm.add_child("last_purchase_table");
							row.invoice_number = r.message[i][0];
							//row.invoice_date = r.message[i][1];
							row.item_code = r.message[i][1];
							row.qty = r.message[i][2];
							row.rate = r.message[i][3];
						}
						cur_frm.refresh_field("last_purchase_table");
						cur_frm.refresh_field("last_supplier_purchase_table");
						cur_frm.refresh_field("quotation_table");
						cur_frm.refresh_field("supplier_quotation_table");
					}
				});
				frappe.call({
					"method": "last_records.last_records.doctype.last_purchase_table.last_purchase_table.getLastpriceSupplier",
					args: {
						item_code: data.item_code,
						supplier: frm.doc.supplier
					},
					callback:function(r){
						var len=r.message.length;
						for (var i=0;i<len;i++){  
							var row = frm.add_child("last_supplier_purchase_table");
							row.invoice_number = r.message[i][0];
							row.supplier_name = r.message[i][1];
							row.invoice_date = r.message[i][2];
							row.item_code = r.message[i][3];
							row.qty = r.message[i][4];
							row.rate = r.message[i][5];
						}
						cur_frm.refresh_field("last_purchase_table");
						cur_frm.refresh_field("last_supplier_purchase_table");
						cur_frm.refresh_field("quotation_table");
						cur_frm.refresh_field("supplier_quotation_table");
					}
				});
				frappe.call({
					"method": "last_records.last_records.doctype.quotation_table.quotation_table.getQuotationprice",
					args: {
							item_code: data.item_code,
							supplier: frm.doc.supplier
					},
					callback:function(r){
						var len=r.message.length;
						for (var i=0;i<len;i++){  
							var row = frm.add_child("quotation_table");
							row.quotation = r.message[i][0];
							//row.invoice_date = r.message[i][1];
							row.item_code = r.message[i][1];
							row.qty = r.message[i][2];
							row.rate = r.message[i][3];
						}
						cur_frm.refresh_field("last_purchase_table");
						cur_frm.refresh_field("last_supplier_purchase_table");
						cur_frm.refresh_field("quotation_table");
						cur_frm.refresh_field("supplier_quotation_table");
					}
				});
				frappe.call({
					"method": "last_records.last_records.doctype.quotation_table.quotation_table.getQuotationpriceSupplier",
					args: {
						item_code: data.item_code,
						supplier: frm.doc.supplier
					},
					callback:function(r){
						var len=r.message.length;
						for (var i=0;i<len;i++){  
							var row = frm.add_child("supplier_quotation_table");
							row.quotation = r.message[i][0];
							row.supplier_name = r.message[i][1];
							row.quotation_date = r.message[i][2];
							row.item_code = r.message[i][3];
							row.qty = r.message[i][4];
							row.rate = r.message[i][5];
						}
						cur_frm.refresh_field("last_purchase_table");
						cur_frm.refresh_field("last_supplier_purchase_table");
						cur_frm.refresh_field("quotation_table");
						cur_frm.refresh_field("supplier_quotation_table");
					}
				});
			})
		})
		frm.add_custom_button(__('Clear Item History'), function(){
			cur_frm.clear_table("last_purchase_table");
			cur_frm.clear_table("last_supplier_purchase_table");
			cur_frm.clear_table("quotation_table");
			cur_frm.clear_table("supplier_quotation_table");
			cur_frm.refresh_field("last_purchase_table");
			cur_frm.refresh_field("last_supplier_purchase_table");
			cur_frm.refresh_field("quotation_table");
			cur_frm.refresh_field("supplier_quotation_table");
		})
	}
});

frappe.ui.form.on("Purchase Order Item",{
	"item_code" : function (frm, cdt, cdn){
		cur_frm.clear_table("last_purchase_table");
			var d2 = locals[cdt][cdn];
		if(d2.item_code){
			frappe.call({
				"method": "last_records.last_records.doctype.last_purchase_table.last_purchase_table.getLastprice",
				args: {
						item_code: d2.item_code,
						supplier: frm.doc.supplier
				},
				callback:function(r){
					var len=r.message.length;
					for (var i=0;i<len;i++){  
						var row = frm.add_child("last_purchase_table");
						row.invoice_number = r.message[i][0];
						//row.invoice_date = r.message[i][1];
						row.item_code = r.message[i][1];
						row.qty = r.message[i][2];
						row.rate = r.message[i][3];
					}
				}
			});
			frappe.call({
				"method": "last_records.last_records.doctype.quotation_table.quotation_table.getQuotationprice",
				args: {
						item_code: d2.item_code,
						supplier: frm.doc.supplier
				},
				callback:function(r){
					var len=r.message.length;
					for (var i=0;i<len;i++){  
						var row = frm.add_child("quotation_table");
						row.quotation = r.message[i][0];
						//row.invoice_date = r.message[i][1];
						row.item_code = r.message[i][1];
						row.qty = r.message[i][2];
						row.rate = r.message[i][3];
					}
				}
			});
			frappe.call({
				"method": "last_records.last_records.doctype.quotation_table.quotation_table.getQuotationpriceSupplier",
				args: {
					item_code: d2.item_code,
					supplier: frm.doc.supplier
				},
				callback:function(r){
					var len=r.message.length;
					for (var i=0;i<len;i++){  
						var row = frm.add_child("supplier_quotation_table");
						row.quotation = r.message[i][0];
						row.supplier_name = r.message[i][1];
						row.quotation_date = r.message[i][2];
						row.item_code = r.message[i][3];
						row.qty = r.message[i][4];
						row.rate = r.message[i][5];
					}
				}
			});
		}
	},
	"rate": function (frm, cdt, cdn){
		cur_frm.clear_table("last_purchase_table");
			var d2 = locals[cdt][cdn];
		if(d2.item_code){
			frappe.call({
				"method": "last_records.last_records.doctype.last_purchase_table.last_purchase_table.getLastprice",
				args: {
						item_code: d2.item_code,
						supplier: frm.doc.supplier
				},
				callback:function(r){
					var trigger_price_alert = false;
					var len=r.message.length;
					for (var i=0;i<len;i++){  
						
						if(d2.rate > r.message[i][4]){
							trigger_price_alert =  true;
						}
						 
					}
					if(trigger_price_alert){
						frappe.msgprint("Rate is higher then past purchase")
					}
				}
			});
		}
	},
});
                	
frappe.ui.form.on("Purchase Order Item",{
	"item_code" : function (frm, cdt, cdn){
		cur_frm.clear_table("last_supplier_purchase_table");
		var d2 = locals[cdt][cdn];
		if(d2.item_code){
			frappe.call({
				"method": "last_records.last_records.doctype.last_purchase_table.last_purchase_table.getLastpriceSupplier",
				args: {
					item_code: d2.item_code,
					supplier: frm.doc.supplier
				},
				callback:function(r){
					var len=r.message.length;
					for (var i=0;i<len;i++){  
						var row = frm.add_child("last_supplier_purchase_table");
						row.invoice_number = r.message[i][0];
						row.supplier_name = r.message[i][1];
						row.invoice_date = r.message[i][2];
						row.item_code = r.message[i][3];
						row.qty = r.message[i][4];
						row.rate = r.message[i][5];
					}
				}
			});
		}
	}
});
frappe.ui.form.on('Purchase Order', {
 setup:function (frm) {
		frm.set_query("tax_category", function () {
		    return {
			    filters: {
			        title: ['in', ['Out State','In State','OUT OF INDIA',]],
			    }
			}
		});
	}
})
frappe.ui.form.on('Purchase Order Item', {
	setup: function(frm) {
		frm.set_query("item_code", function() {
			return {
				filters: [
					["Item","workflow_state", "in", ["Checked","Approved","Old Item"]]
				]
			}
		});
	}
});