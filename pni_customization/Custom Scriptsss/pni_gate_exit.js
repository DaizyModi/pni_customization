frappe.ui.form.on('PNI Gate Exit', {
    refresh: function (frm) {
        if (!cur_frm.doc.__islocal) {
            if (frm.doc.vehicle_gate_entry_time == '0:00:00' && frm.doc.vehicle_gate_exit_time == '0:00:00') {
                frm.add_custom_button(__('In Time'), function () {
                    frm.set_value("vehicle_gate_entry_time", frappe.datetime.now_time());
                    frm.save();
                });
            }
            else if (frm.doc.vehicle_gate_entry_time != '0:00:00' && frm.doc.vehicle_gate_exit_time == '0:00:00') {
                frm.add_custom_button(__('Out Time'), function () {
                    frm.set_value("vehicle_gate_exit_time", frappe.datetime.now_time());
                    frm.save();
                });
            }
        }
    }
})