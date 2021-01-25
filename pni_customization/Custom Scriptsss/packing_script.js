frappe.ui.form.on('Packing', {
	setup:function (frm){
		frm.set_query ("item", "packing_table",function(){
			return{
				filters:{
					"item_group":"Paper Blank"
				}
			}
		})
	}
})