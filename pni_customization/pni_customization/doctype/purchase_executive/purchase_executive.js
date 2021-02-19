// Copyright (c) 2021, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Executive', {
    // refresh: function(frm) {

    // }
});
// cur_frm.cscript.refresh = function (doc, cdt, cdn) {
//     cur_frm.cscript.set_root_readonly(doc);
// }

// cur_frm.cscript.set_root_readonly = function (doc) {
//     // read-only for root
//     if (!doc.parent_purchase_executive && !doc.__islocal) {
//         cur_frm.set_read_only();
//         cur_frm.set_intro(__("This is a root Purchase Executive and cannot be edited."));
//     } else {
//         cur_frm.set_intro(null);
//     }
// }

// //get query select purchase executive
// cur_frm.fields_dict['parent_purchase_executive'].get_query = function (doc, cdt, cdn) {
//     return {
//         filters: [
//             ['Purchase Executive', 'is_group', '=', 1],
//             ['Purchase Executive', 'name', '!=', doc.purchse_executive_name]
//         ]
//     }
// }

// cur_frm.fields_dict.employee.get_query = function (doc, cdt, cdn) {
//     return { query: "erpnext.controllers.queries.employee_query" }
// }
