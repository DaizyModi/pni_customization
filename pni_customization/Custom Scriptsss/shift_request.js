frappe.ui.form.on("Shift Request", {
    employee: function (frm) {
        var shift_array = new Array();
        frappe.call({
            'method': 'pni_customization.utility.shift_request_utility.get_shift_detail',
            args: {
                name: frm.doc.employee
            },
            callback: function (r) {
                console.log(r.message);
                for (var i = 0; i < r.message.length; i++) {
                    shift_array.push(r.message[i].shift_type);
                }
                frm.doc.shift_array = shift_array;
            }
        })
    },
    setup: function (frm) {
        debugger;
        frm.set_query("shift_type", function (frm) {
            return {
                filters: [
                    ['shift_type', 'in', cur_frm.doc.shift_array]
                ]
            }
        })

    }
});