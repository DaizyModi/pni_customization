// Copyright (c) 2019, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('PNI Gate Entry', {
    refresh: function (frm) {
        if (!frm.doc.created_by) {
            debugger;
            cur_frm.set_value("created_by", frappe.session.user);
        }
    },
    purchase_order: function (frm) {
        frappe.call({
            "method": "pni_customization.pni_customization.doctype.pni_gate_entry.pni_gate_entry.get_po_items",
            args: {
                po: cur_frm.doc.purchase_order
            },
            callback: function (r) {
                if (r.message) {
                    console.log(r.message)
                    frm.clear_table('items');
                    r.message.forEach(i => {
                        let row = frm.add_child('items');
                        row.item_code = i.item_code;
                        row.item_name = i.item_name;
                        row.qty = i.item_qty;
                        row.uom = i.item_uom;
                    });
                    refresh_field('items');
                }
                else {
                    debugger;
                    cur_frm.set_value('purchase_order', '');
                    refresh_field('purchase_order');
                }
            }
        })
    }
});
