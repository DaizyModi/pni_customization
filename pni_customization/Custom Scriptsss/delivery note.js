frappe.ui.form.on("Delivery Note Item", {
    "item_code": function (frm, cdt, cdn) {
        var d2 = locals[cdt][cdn];

        if (d2.price_list_rate > 0) {
            d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor)
            frm.refresh_field("items")
        }
    },
    "is_paper_plate": function (frm, cdt, cdn) {
        var d2 = locals[cdt][cdn];
        if (d2.price_list_rate > 0) {
            d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor)
            frm.refresh_field("items")
        }
    },
    "paper_cup": function (frm, cdt, cdn) {
        var d2 = locals[cdt][cdn];
        if (d2.price_list_rate > 0) {
            d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor)
            frm.refresh_field("items")
        }
    },
    "base_uom_rate": function (frm, cdt, cdn) {
        var d2 = locals[cdt][cdn];

        if (parseFloat(d2.base_uom_rate * d2.conversion_factor) < d2.price_list_rate && d2.price_list_rate > 0) {
            frappe.msgprint("[Warning] Rate is less then " + parseFloat(d2.price_list_rate / d2.conversion_factor))
        }

        d2.rate = parseFloat(d2.base_uom_rate * d2.conversion_factor)
        frm.refresh_field("items")
    },
    "rate": function (frm, cdt, cdn) {
        var d2 = locals[cdt][cdn];
        if (d2.rate < d2.price_list_rate && d2.price_list_rate > 0) {
            frappe.msgprint("[Warning] Rate is less then " + d2.price_list_rate)
            // d2.base_uom_rate = parseFloat(d2.price_list_rate / d2.conversion_factor	)
        }
    }
});

frappe.ui.form.on('Delivery Note', {
    refresh(frm) {
        frm.doc.items.forEach(function (element) {
            if (element.price_list_rate > element.rate && element.price_list_rate > 0 && !element.approve_law_rate__) {
                //frappe.msgprint("[Warning] Item "+element.item_code +"'s rate is lower then Item Price List");
            }
        })
        if (frm.doc.is_return && frm.doc.__islocal) {
            frm.set_value("naming_series", "MAT-CRN-.2020.-");
        }
        const doc = frm.doc;
        debugger;
        if (doc.payment_terms_template && !doc.payment_schedule.length && frm.doc.__islocal) {
            var posting_date = doc.posting_date || doc.transaction_date;
            frappe.call({
                method: "erpnext.controllers.accounts_controller.get_payment_terms",
                args: {
                    terms_template: doc.payment_terms_template,
                    posting_date: posting_date,
                    grand_total: doc.rounded_total || doc.grand_total,
                    bill_date: doc.bill_date
                },
                callback: function (r) {
                    if (r.message && !r.exc) {
                        frm.set_value("payment_schedule", r.message);
                    }
                }
            })
        }
        if ((cur_frm.doc.naming_series == "FOC-DN-.2020-" || cur_frm.doc.naming_series == "FOC-DN-.YYYY.-") && cur_frm.doc.status != "Closed" && !cur_frm.doc.__islocal && !cur_frm.doc.disable_auto_close) {
            status = "Closed"
            frappe.ui.form.is_saving = true;
            frappe.call({
                method: "erpnext.stock.doctype.delivery_note.delivery_note.update_delivery_note_status",
                args: { docname: frm.doc.name, status: status },
                callback: function (r) {
                    if (!r.exc)
                        frm.reload_doc();
                },
                always: function () {
                    frappe.ui.form.is_saving = false;
                }
            })
        }
    },
    is_foc(frm) {
        if (frm.doc.is_foc) {
            frm.set_value("naming_series", "FOC-DN-.2020-");
        } else {
            frm.set_value("naming_series", "MAT-DN-.2020-")
        }
    },
    payment_terms_template: function (frm) {
        debugger;
        const doc = frm.doc;
        if (doc.payment_terms_template) {
            var posting_date = doc.posting_date || doc.transaction_date;
            frappe.call({
                method: "erpnext.controllers.accounts_controller.get_payment_terms",
                args: {
                    terms_template: doc.payment_terms_template,
                    posting_date: posting_date,
                    grand_total: doc.rounded_total || doc.grand_total,
                    bill_date: doc.bill_date
                },
                callback: function (r) {
                    if (r.message && !r.exc) {
                        frm.set_value("payment_schedule", r.message);
                    }
                }
            })
        }
    }
});
frappe.ui.form.on('Delivery Note', {
    validate: function (frm) {
        $.each(frm.doc.sales_team, function (i, d) {
            frm.set_value("sales_person_name", d.sales_person);
        });
        var wip = false;
        $.each(frm.doc.items, function (i, d) {
            if (!d.against_sales_order) {
                wip = true;
            }
        });
        if (wip) {
            cur_frm.set_value("wip", wip);
        }
        cur_frm.refresh();
    }
});
frappe.ui.form.on('Delivery Note', {
    setup: function (frm) {
        frm.set_query("tax_category", function () {
            return {
                filters: {
                    title: ['in', ['Out State', 'In State', 'OUT OF INDIA',]],
                }
            }
        });
    }
})