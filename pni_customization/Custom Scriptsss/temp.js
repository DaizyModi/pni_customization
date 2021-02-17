frappe.ui.form.on('Sales Order', {
    refresh: function (frm) {
        frm.set_query("item_code", "items", function (doc, cdt, cdn) {
            debugger;
            // var row = locals[cdt][cdn];
            // if (row.sales_invoice) {
            return {
                query: 'pni_customization.utility.customer_complaint_form_utility.get_items',
                filters: { "sales_invoice": "SAL-ORD-2020-00005" }
            };
            // }
        });
    }
})