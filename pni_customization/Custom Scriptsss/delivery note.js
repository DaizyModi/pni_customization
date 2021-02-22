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
    refresh: function (frm) {
        frm.doc.items.forEach(function (element) {
            if (element.price_list_rate > element.rate && element.price_list_rate > 0 && !element.approve_law_rate__) {
                //frappe.msgprint("[Warning] Item "+element.item_code +"'s rate is lower then Item Price List");
            }
        })
        if (frm.doc.is_return && frm.doc.__islocal) {
            frm.set_value("naming_series", "MAT-CRN-.2020.-");
        }
        if (!cur_frm.doc.__islocal && frm.doc.name) {
            frm.set_df_property('is_foc', 'read_only', 1)
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
        cur_frm.set_value("wip", wip);
        cur_frm.refresh();
    }
});
frappe.ui.form.on('Delivery Note', {
    setup: function (frm) {
        // cur_frm.cscript.setup_allow_bulk_edit2()
        frm.set_query("tax_category", function () {
            return {
                filters: {
                    title: ['in', ['Out State', 'In State', 'OUT OF INDIA',]],
                }
            }
        });
        if (!cur_frm.doc.__islocal && frm.doc.name) {
            frm.set_df_property('is_foc', 'read_only', 1)
        }

    }
})

cur_frm.cscript.setup_allow_bulk_edit2 = function () {
    var me = this;
    if (this.frm) {
        // download
        cur_frm.cscript.setup_download()

        // upload
        frappe.flags.no_socketio = true;
        $(this.wrapper).find(".grid-upload").removeClass('hidden').on("click", function () {
            new frappe.ui.FileUploader({
                as_dataurl: true,
                allow_multiple: false,
                on_success(file) {
                    var data = frappe.utils.csv_to_array(frappe.utils.get_decoded_string(file.dataurl));
                    // row #2 contains fieldnames;
                    var fieldnames = data[2];

                    me.frm.clear_table(me.df.fieldname);
                    $.each(data, function (i, row) {
                        if (i > 6) {
                            var blank_row = true;
                            $.each(row, function (ci, value) {
                                if (value) {
                                    blank_row = false;
                                    return false;
                                }
                            });

                            if (!blank_row) {
                                var d = me.frm.add_child(me.df.fieldname);
                                $.each(row, function (ci, value) {
                                    var fieldname = fieldnames[ci];
                                    var df = frappe.meta.get_docfield(me.df.options, fieldname);

                                    // convert date formatting
                                    if (df.fieldtype === "Date" && value) {
                                        value = frappe.datetime.user_to_str(value);
                                    }

                                    if (df.fieldtype === "Int" || df.fieldtype === "Check") {
                                        value = cint(value);
                                    }

                                    d[fieldnames[ci]] = value;
                                });
                            }
                        }
                    });

                    me.frm.refresh_field(me.df.fieldname);
                    frappe.msgprint({ message: __('Table updated'), title: __('Success'), indicator: 'green' })
                }
            });
            return false;
        });
    }
}

cur_frm.cscript.setup_download = function () {
    var me = this;
    let title = me.df.label || frappe.model.unscrub(me.df.fieldname);
    $(this.wrapper).find(".grid-download").removeClass('hidden').on("click", function () {
        var data = [];
        var docfields = [];
        data.push([__("Bulk Edit {0}", [title])]);
        data.push([]);
        data.push([]);
        data.push([]);
        data.push([__("The CSV format is case sensitive")]);
        data.push([__("Do not edit headers which are preset in the template")]);
        data.push(["------"]);
        $.each(frappe.get_meta(me.df.options).fields, function (i, df) {
            // don't include the read-only field in the template
            if (frappe.model.is_value_type(df.fieldtype)) {
                data[1].push(df.label);
                data[2].push(df.fieldname);
                let description = (df.description || "") + ' ';
                if (df.fieldtype === "Date") {
                    description += frappe.boot.sysdefaults.date_format;
                }
                data[3].push(description);
                docfields.push(df);
            }
        });

        // add data
        $.each(me.frm.doc[me.df.fieldname] || [], function (i, d) {
            var row = [];
            $.each(data[2], function (i, fieldname) {
                var value = d[fieldname];

                // format date
                if (docfields[i].fieldtype === "Date" && value) {
                    value = frappe.datetime.str_to_user(value);
                }

                row.push(value || "");
            });
            data.push(row);
        });

        frappe.tools.downloadify(data, null, title);
        return false;
    });
}