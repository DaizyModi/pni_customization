frappe.ui.form.on('Installation Note', {
    refresh(frm) {
        // your code here
    },
    pre_installation_check: function (frm) {
        frappe.call({
            "method": "pni_customization.utility.installation_note.get_pre_installation_check_item",
            args: {
                pre_installation_check: frm.doc.pre_installation_check
            },
            callback: function (r) {
                if (r.message) {
                    cur_frm.doc.installation_note_item_details = {}
                    r.message.forEach(function (element) {
                        var c = frm.add_child("installation_note_item_details");
                        c.particular = element.particular;
                        c.qty_per_machine = element.qty_per_machine;
                    });
                    refresh_field("installation_note_item_details");
                }
            }
        })
    },
})