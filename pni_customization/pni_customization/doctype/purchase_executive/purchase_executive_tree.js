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
    onrender: function (node) {
        if (!node.is_root) {
            debugger;
            frappe.call({
                'method': 'pni_customization.pni_customization.doctype.purchase_executive.purchase_executive.get_amount',
                'args': {
                    'name': node.data.value
                },
                callback: function (r) {
                    if (r.message) {
                        console.log(r.message)
                        if (node.data && r.message !== undefined) {
                            $('<span class="balance-area pull-right text-muted small">'
                                + format_currency(Math.abs(r.message), node.data.company_currency)
                                + '</span>').insertBefore(node.$ul);
                        }
                    }
                    else {
                        $('<span class="balance-area pull-right text-muted small">'
                            + format_currency(Math.abs(0), node.data.company_currency)
                            + '</span>').insertBefore(node.$ul);
                    }
                }
            })

        }
    }
}