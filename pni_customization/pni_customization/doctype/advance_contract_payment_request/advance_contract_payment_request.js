// Copyright (c) 2021, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Advance Contract Payment Request', {
    // refresh: function (frm) {

    // }
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
    },
    person_name: function (frm) {
        frappe.call({
            method: "calculate_allow_amount",
            doc: frm.doc,
            callback: function (r) {
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
