// Copyright (c) 2020, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Update Shift Request', {
    // refresh: function(frm) {

    // }
    shift_type: function (frm) {
        var emp_array = "";
        frappe.call({
            "method": "pni_customization.pni_customization.doctype.update_shift_request.update_shift_request.get_employees",
            args: {
                shift_type: frm.doc.shift_type
            },
            callback: function (r) {
                console.log(r.message);
                for (var i = 0; i < r.message.length; i++) {
                    emp_array += r.message[i][0] + ",";
                }
                debugger;
                console.log(emp_array);
                frm.set_value("emp_array", emp_array);
            }
        })
    },
    setup: function (frm) {
        frm.set_query("employee", 'shift_employee_table', function (doc, cdt, cdn) {
            debugger;
            return {
                filters: [
                    ['name', 'in', frm.doc.emp_array]
                ]
            }
        })
    }
});