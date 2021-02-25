frappe.ui.form.on("Shift Assignment", {
    employee: function (frm) {
        var shift_array = "";
        frappe.call({
            'method': 'pni_customization.utility.shift_request_utility.get_shift_detail',
            args: {
                name: frm.doc.employee
            },
            callback: function (r) {
                console.log(r.message);
                for (var i = 0; i < r.message.length; i++) {
                    shift_array += r.message[i].shift_type + ",";
                }
                debugger;
                frm.set_value("shift_array", shift_array);
            }
        })
    },
    setup: function (frm) {
        debugger;
        frm.set_query("shift_type", function (frm) {
            return {
                filters: [
                    ['name', 'in', cur_frm.doc.shift_array]
                ]
            }
        })

    }
});