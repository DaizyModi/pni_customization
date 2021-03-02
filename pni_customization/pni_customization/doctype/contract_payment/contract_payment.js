// Copyright (c) 2021, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contract Payment', {
    // refresh: function (frm) {
    // },
    setup: function (frm) {
        frm.set_query("person_name", function () {
            if (frm.doc.person_type == "Employee") {
                debugger;
                return {
                    filters: {
                        "is_on_contract": 1
                    }
                }
            }
        });
        frm.set_query("advance_payment_request", function () {
            if (frm.doc.is_advance_payment) {
                return {
                    filters: {
                        'docstatus': 1,
                        'person_name': frm.doc.person_name
                    }
                }
            }
        })
    }
});
