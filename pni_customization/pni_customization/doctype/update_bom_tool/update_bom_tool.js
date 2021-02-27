// Copyright (c) 2021, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Update BOM Tool', {
    // refresh: function(frm) {

    // }
    get_bom: function (frm) {
        frappe.call({
            "method": "get_bom",
            doc: cur_frm.doc,
            callback: function (r) {
                console.log(r.message);
                frm.reload_doc()
            }
        })
    },
    get_new_bom: function (frm) {
        frappe.call({
            "method": "get_new_bom",
            doc: cur_frm.doc,
            callback: function (r) {
                console.log(r.message);
                frm.reload_doc()
            }
        })
    },
    replace_bom: function (frm) {
        frappe.call({
            "method": "replace_bom",
            doc: cur_frm.doc,
            callback: function (r) {
                console.log(r.message);
                frm.reload_doc()
            }
        })
    }
});
