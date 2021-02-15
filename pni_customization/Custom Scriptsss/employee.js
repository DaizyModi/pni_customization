frappe.ui.form.on('Employee', {
    setup: function (frm) {
        frm.set_query("default_shift", function () {
            return {
                filters: {
                    "shift_status": "Enable"
                }
            }
        });
        frm.set_query("salary_structure_assignment", function () {
            return {
                filters: {
                    "employee": frm.doc.name,
                    "docstatus": 1
                }
            }
        });
    },
    is_on_contract(frm) {
        if (frm.doc.is_on_contract) {
            frm.set_df_property('contract_department', 'reqd', 1)
        } else {
            frm.set_df_property('contract_department', 'reqd', 0)
        }

    },
    is_overtime_calculate(frm) {
        if (frm.doc.is_overtime_calculate) {
            frm.set_df_property('overtime_', 'reqd', 1)
        } else {
            frm.set_df_property('overtime_', 'reqd', 0)
        }

    },
    status(frm) {
        if (frm.doc.status == "Active") {
            frm.set_df_property('duty_hour', 'reqd', 1)
        } else {
            frm.set_df_property('duty_hour', 'reqd', 0)
        }

    },
    has_pf(frm) {
        if (frm.doc.has_pf) {
            frm.set_df_property('uan_no', 'reqd', 1)
        } else {
            frm.set_df_property('uan_no', 'reqd', 0)
        }

    },
})
frappe.ui.form.on('Employee', {
    setup: function (frm) {
        frm.set_query("employee_onboarding_process", function () {
            return {
                filters: { "boarding_status": "Completed" }
            }
        });
    }
})
frappe.ui.form.on('Employee', {
    refresh(frm) {
        frm.add_custom_button(__('Open Job Application'), function () {
            frappe.set_route("List", "Job Application", { "name": frm.doc.job_application });
        });
    }
});