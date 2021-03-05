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
                        'person_name': frm.doc.person_name,
                        'payment_required_by': ['between', [frm.doc.from_date, frm.doc.to_date]]
                    }
                }
            }
        })
    },
    month: function (frm) {
        frappe.call({
            method: "get_apr_by_month",
            doc: frm.doc,
            callback: function (r) {
                console.log(r.message);
                frm.set_value('from_date', r.message[0]);
                frm.set_value('to_date', r.message[1]);
            }
        })
        frappe.call({
            method: "calculate_paid_amount",
            doc: frm.doc,
            callback: function (r) {
                console.log(r.message)
                if (r.message) {
                    frm.set_value('allow_advance', r.message);
                }
                else {
                    frm.set_value('allow_advance', 0);
                }
            }
        })
    },
    person_name: function (frm) {
        frappe.call({
            method: "calculate_paid_amount",
            doc: frm.doc,
            callback: function (r) {
                console.log(r.message)
                if (r.message) {
                    frm.set_value('allow_advance', r.message);
                }
                else {
                    frm.set_value('allow_advance', 0);
                }
            }
        })
    },
    year: function (frm) {
        frappe.call({
            method: "calculate_paid_amount",
            doc: frm.doc,
            callback: function (r) {
                console.log(r.message)
                if (r.message) {
                    frm.set_value('allow_advance', r.message);
                }
                else {
                    frm.set_value('allow_advance', 0);
                }
            }
        })
    },
    person_type: function (frm) {
        frappe.call({
            method: "calculate_paid_amount",
            doc: frm.doc,
            callback: function (r) {
                console.log(r.message)
                if (r.message) {
                    frm.set_value('allow_advance', r.message);
                }
                else {
                    frm.set_value('allow_advance', 0);
                }
            }
        })
    }
});
