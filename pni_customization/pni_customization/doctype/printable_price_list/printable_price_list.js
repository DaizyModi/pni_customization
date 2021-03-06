// Copyright (c) 2021, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Printable Price List', {
    // refresh: function (frm) {

    // }
});
frappe.ui.form.on('PPL Paper Cup', {
    brand: function (frm, cdt, cdn) {
        get_price_list(frm, cdt, cdn);
    }
})

let get_price_list = function (frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    frappe.call({
        "method": 'pni_customization.pni_customization.doctype.printable_price_list.printable_price_list.get_price_list',
        args: {
            brand: d.brand
        },
        callback: function (r) {
            d.rate_per_piece = r.message[0][1];
            d.price_1000 = r.message[0][2];
            d.gst18 = r.message[0][3];
            d.total_price = r.message[0][4];
            frm.refresh_field('paper_cup_t');
        }
    })
}


