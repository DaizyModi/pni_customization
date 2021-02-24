frappe.ui.form.on('Complaint Items', {
    sales_invoice: function name(frm) {
        get_invoice_items(frm, cdt, cdn);
    },
})
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
            var data_temp = cur_frm.doc.paper_details.filter(obj => {
                return obj.name === cdn
            })
            var items;
            if (row.sales_invoice) {
                get_invoice_items(frm, cdt, cdn);
                console.log(data_temp[0]);
                console.log(row.item_array);
                debugger;
                return {
                    filters: [
                        ['item_code', 'in', data_temp[0].item_array]
                    ]
                }
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

let get_invoice_items = function (frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    var items = new Array();
    frappe.call({
        method: 'pni_customization.utility.customer_complaint_form_utility.get_invoice_items',
        args: {
            sales_invoice: d.sales_invoice
        },
        callback: function (r) {

            for (var i = 0; i < r.message.length; i++) {
                items.push(r.message[i].item_code);
            }

            console.log(items);
            d.item_array = items;
        }
    })
}