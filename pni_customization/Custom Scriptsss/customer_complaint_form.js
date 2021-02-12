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
                    // query: 'frappe.contacts.doctype.address.address.address_query',
                    filters: {
                        sales_invoice: row.sales_invoice
                    }
                };
            }
        })
    }
})