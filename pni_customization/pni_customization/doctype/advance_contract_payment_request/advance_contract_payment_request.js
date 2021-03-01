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
    }
});
