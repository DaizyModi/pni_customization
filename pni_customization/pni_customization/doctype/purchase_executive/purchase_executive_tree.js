frappe.provide("frappe.treeview_settings");
frappe.treeview_settings['Purchase Executive'] = {
    fields: [
        {
            fieldtype: 'Data',
            fieldname: 'purchase_executive_name',
            label: __('New Purchase Executive'),
            reqd: true
        },
        {
            fieldtype: 'Link',
            fieldname: 'employee',
            label: __('Employee'),
            options: 'Employee',
            description: __("Please enter Employee Id of this Purchase Executive")
        },
        {
            fieldtype: 'Check',
            fieldname: 'is_group',
            label: __('Group Node'),
            description: __("Further Executives can be only created under 'Group' type nodes")
        }
    ],
}