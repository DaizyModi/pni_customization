frappe.ui.form.on('Customer Complaint Form', {
    refresh(frm) {
        // your code here
    },
    setup: function (frm) {
        frm.set_query("serial_no", "installed_items", function () {
            return {
                filters: {
                    customer: frm.doc.customer
                }
            }
        });
        frm.set_query("sales_invoice", "paper_details", function () {
            return {
                filters: {
                    customer: frm.doc.customer
                }
            }
        });
        frm.set_query("item_code", "paper_details", function (doc, cdt, cdn) {
            debugger;
            var row = locals[cdt][cdn];
            if (row.sales_invoice) {
                return {
                    query: 'pni_customization.utility.customer_complaint_form_utility.get_items',
                    filters: { "sales_invoice": row.sales_invoice }
                };
            }
        });
        frm.set_query('serial_no', "table_38", function () {
            debugger;
            var list_of_serial = new Array();
            for (var i = 0; i < frm.doc.installed_items.length; i++) {
                list_of_serial.push(frm.doc.installed_items[i].serial_no)
            }
            return {
                filters: [
                    ['serial_no', 'in', list_of_serial]
                ]
            }
        })
    }
})

// let get_invoice_items = function (frm) {
//     let list_items = new Array();
//     frappe.call({
//         'method': frappe.client
//     })
// }
// // frappe.ui.form.on('Complaint Items', {
//     sales_invoice: function (doc, cdt, cdn) {
//         // debugger;
//         var me = this;
//         var d2 = locals[cdt][cdn];
//         debugger;
//         me.frm.set_query("item_code", "paper_details", function (doc, cdt, cdn) {
//             return {
//                 filters: {
//                     sales_invoice: d2.sales_invoice
//                 }
//             }
//         });
//     }
// })