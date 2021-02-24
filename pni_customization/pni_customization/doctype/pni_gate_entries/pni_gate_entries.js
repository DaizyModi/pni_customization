// Copyright (c) 2021, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Gate Entries', {
    refresh: function (frm) {
        if (!frm.doc.created_by) {
            frm.set_value('created_by', frappe.session.user);
        }
    },
    setup: function (frm) {
        frm.set_query('purchase_order', function () {
            return {
                filters: {
                    'supplier': frm.doc.supplier_name
                }
            }
        })
    }
});
