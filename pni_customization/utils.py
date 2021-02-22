import frappe
import json
from frappe.model.mapper import get_mapped_doc
from frappe import _
from frappe.utils import flt
from pni_customization.pni_customization.doctype.pni_sales_order.pni_sales_order import update_delivery_pni_sales_order
from pni_customization.pni_customization.doctype.pni_quality_inspection.pni_quality_inspection import update_work_order
from pni_customization.utility.purchase_order_utility import validate_purchase_order


def validate_item_price(doc, method):
    if doc.brand and doc.selling and not doc.customer:
        value = frappe.db.get_value("Brand Group Table",
                                    {
                                        "brand": doc.brand,
                                    }, "selling_rate")
        if value and float(value) > 0:
            doc.price_list_rate = value


def validate_reel_qty(doc):
    items_calc = {}
    for item in doc.items:
        if item.is_reel_item:
            if not doc.reel_table_purchase:
                frappe.throw("Reel Entry needed for Item "+item.item_code)
            if not item.reel_brand:
                frappe.throw(
                    "Reel Brand is Mandatory for Item " + item.item_code)
            weight = items_calc.setdefault(
                item.item_code, {}).setdefault(item.reel_brand, 0)
            items_calc[item.item_code][item.reel_brand] = weight + \
                float(item.qty)
    item_reel_calc = {}
    for reel in doc.reel_table_purchase:
        weight = item_reel_calc.setdefault(
            reel.item, {}).setdefault(reel.brand, 0)
        item_reel_calc[reel.item][reel.brand] = weight + reel.weight

    for _data in items_calc:
        for data in items_calc.get(_data):
            if item_reel_calc.get(_data).get(data) and items_calc.get(_data).get(data):
                reel_weight = item_reel_calc.get(_data).get(data)
                reel_weight -= doc.tear_weight
                if (int(reel_weight)+1) < int(items_calc.get(_data).get(data)):
                    frappe.throw("Total Reel Qty {1} for item  {0} is less then {2} ".format(
                        data, reel_weight, items_calc.get(_data).get(data)))
                if int(reel_weight) > (int(items_calc.get(_data).get(data))+1):
                    frappe.throw("Total Reel Qty {1} for item  {0} is more then {2} ".format(
                        data, reel_weight, items_calc.get(_data).get(data)))
    frappe.errprint("items_calc")
    frappe.errprint(items_calc)
    frappe.errprint("item_reel_calc")
    frappe.errprint(item_reel_calc)


def validate_so(doc, method):
    outstanding_amt = 0
    for row in doc.customer_outstanding:
        outstanding_amt += float(row.outstanding_amt)
    doc.total_customer_outstanding = outstanding_amt
    doc.need_approval = False
    for item in doc.items:
        if not (item.price_list_rate > 0):
            frappe.throw("Price List Rate not available for " + item.item_code)
        if item.is_paper_plate or item.paper_cup:
            if not(item.base_uom_rate > 0):
                frappe.throw(
                    "Paper Cup and Plate Rate can't be zero for " + item.item_code)
            item.rate = float(item.base_uom_rate) * \
                float(item.conversion_factor)
        if round(item.rate, 4) < round(item.price_list_rate, 4):
            item.need_approval = True
            doc.need_approval = True
            frappe.errprint(item)
            frappe.errprint(item.rate)
            frappe.errprint(item.price_list_rate)
        else:
            item.need_approval = False
        item.unit_price_pni = float(
            float(item.price_list_rate) / float(item.conversion_factor))

    if doc.workflow_state == "Pending For Accounts Approval":
        for item in doc.items:
            if round(item.rate, 4) < round(item.price_list_rate, 4) and round(item.price_list_rate, 4) > 0:
                if not item.approve_law_rate__:
                    frappe.throw(
                        "Item {0}'s low rate is not approved by management.".format(item.item_code))


def validate_reel(doc, method):
    total_weight = 0
    for reel in doc.reel_table_purchase:
        total_weight += float(reel.weight)
    doc.total_reel_weight = float(total_weight)


def create_reel(doc, method):
    update_pni_gate_entry(doc, method)
    validate_reel_qty(doc)
    if doc.reel_item:
        for item in doc.reel_table_purchase:
            doc = frappe.get_doc({
                "doctype": "Reel",
                "status": "In Stock",
                "reel_id": item.reel_id,
                "posting_date": doc.posting_date,
                "supplier_reel_id": item.reel_id,
                "warehouse": item.accepted_warehouse,
                "item": item.item,
                "type": "Blank Reel",
                "blank_weight": item.weight,
                "brand": item.brand,
                "weight": item.weight
            })
            doc.insert(ignore_permissions=True)
            doc.submit()


def cancel_reel(doc, method):
    if doc.reel_item:
        for item in doc.reel_table_purchase:
            reel_out = frappe.get_doc("Reel", item.reel_id)
            reel_out.cancel()
            reel_out.delete()


def get_permission_query_conditions_for_lead(user):
    if "System Manager" in frappe.get_roles(user):
        return None
    elif "Lead Management Role" in frappe.get_roles(user):
        return None
    elif "Sales User" in frappe.get_roles(user):
        # if is_sales_person_group():
        # 	return """
        # 		(tabLead.owner in ({user}) )
        # 	""".format(user=is_sales_person_group())
        return """
		(tabLead.owner = '{user}' ) 
		or 
		(tabLead._assign like '%{user}%')
		""".format(user=user)


def get_permission_query_conditions_for_purchase_order(user):
    if "System Manager" in frappe.get_roles(user):
        return None
    elif "Purchase Executive" in frappe.get_roles(user):
        allow = []
        allow = get_allow_pe(user)
        return """
		`tabPurchase Order`.purchasse_executive in '{user}' 
		""".format(allow=allow)


def get_allow_pe(user):
    # return list of allo pe
    return []


def get_permission_query_conditions_for_opportunity(user):
    if "System Manager" in frappe.get_roles(user):
        return None
    elif "Sales User" in frappe.get_roles(user):
        # if is_sales_person_group():
        # 	return """
        # 		(tabOpportunity.owner in ({user}) )
        # 	""".format(user=is_sales_person_group())
        return """
		(tabOpportunity.owner = '{user}' ) 
		or 
		(tabOpportunity._assign like '%{user}%')
		""".format(user=user)


def is_sales_person_group():
    sales_person = frappe.get_value(
        "Sales Person", {"pni_user": frappe.session.user})
    if not sales_person:
        return False
    is_group = frappe.get_value(
        "Sales Person", {"pni_user": frappe.session.user}, "is_group")
    if is_group:
        data = frappe.get_all(
            "Sales Person", {"parent_sales_person": "Ravi Singh Rawat"}, ["pni_user"])
        datas = "','".join([item['pni_user'] for item in data])
        datas += "','"+str(frappe.session.user)
        datas = "'"+datas + "'"
        return datas
    else:
        return False


@frappe.whitelist()
def get_packing(packing, doctype):
    packing_doc = frappe.get_doc(doctype, packing)

    if packing_doc and (packing_doc.status == "Available" or packing_doc.status == "In Stock"):
        return packing_doc
    else:
        frappe.throw(str(doctype) + " Not Available with "+packing_doc.name)


@frappe.whitelist()
def get_pni_bags(item, qty, weight=0, packing_category=None, warehouse=None):
    filters = {
        'item': item,
        'status': 'In Stock',
        'docstatus': 1
    }
    if float(weight) > 0:
        filters['weight'] = weight
    if packing_category:
        filters['packing_category'] = packing_category
    if warehouse:
        filters['warehouse'] = warehouse

    bags = frappe.get_all("PNI Bag",
                          filters=filters,
                          fields=['name', 'item', 'weight'],
                          limit_page_length=qty
                          )

    return bags


@frappe.whitelist()
def get_item_data(item):
    # return item data
    item_doc = frappe.get_doc("Item", item)
    attribute_data = {}
    for row in item_doc.attributes:
        attribute_doc = frappe.get_doc("Item Attribute", row.attribute)

        values = []
        for attr_value in attribute_doc.item_attribute_values:
            values.append(attr_value.attribute_value)

        if not attribute_doc.numeric_values:
            attribute_data.update(
                {row.attribute: {"numeric_values": False, "values": values}})
        else:
            attribute_data.update(
                {row.attribute: {"numeric_values": True, "values": []}})

    return {
        "item": item,
        "attribute_data": attribute_data
    }


@frappe.whitelist()
def get_item(item, values):
    attributes = json.loads(values)
    items = frappe.get_all("Item", {"variant_of": item})
    for item in items:
        is_varient = True
        item_doc = frappe.get_doc("Item", item)
        for varient_attribute in item_doc.attributes:
            if str(varient_attribute.attribute_value) != str(attributes[varient_attribute.attribute]):
                is_varient = False
        if is_varient == True:
            return item_doc
    return frappe.throw("Item Not Found")


@frappe.whitelist()
def update_item(doc, method):
    pass
    # if doc.item_group == "Paper Cup" and doc.variant_of:
    # 	for atr in doc.attributes:
    # 		if atr.attribute == "PC-Packing":
    # 			frappe.db.set_value("Item", doc.name, "stack_size", str(atr.attribute_value))
    # 			frappe.db.commit()


@frappe.whitelist()
def make_pni_quotation(source_name, target_doc=None, ignore_permissions=False):
    lead = frappe.get_doc("Lead", source_name)
    customer = frappe.db.get_value("Customer", {"lead_name": lead.name})

    def set_missing_values(source, target):
        if customer:
            target.customer = customer

    doclist = get_mapped_doc("Lead", source_name, {
        "Lead": {
            "doctype": "PNI Quotation",
            "field_map": {
                "name": "lead",
            }
        }
    }, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

    return doclist


@frappe.whitelist()
def make_pni_quotation_from_opportunity(source_name, target_doc=None, ignore_permissions=False):
    opportunity = frappe.get_doc("Opportunity", source_name)
    lead = frappe.get_doc("Lead", opportunity.party_name)
    customer = frappe.db.get_value("Customer", {"lead_name": lead.name})
    if not customer:
        frappe.throw("Please Create Customer first from Lead")

    def set_missing_values(source, target):
        if customer:
            target.customer = customer

    doclist = get_mapped_doc("Opportunity", source_name, {
        "Opportunity": {
            "doctype": "PNI Quotation",
            "field_map": {
                "party_name": "lead",
                "name": "opportunity"
            }
        }
    }, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

    return doclist


def sales_invoice_validate(doc, method):
    receipt_date = receipt_amt = commitment_date = commitment_amt = remark = receipt_date = ""
    for row in doc.daily_payment_report:
        commitment_date = row.commitment_date
        commitment_amt = row.commitment_amt
        remark = row.remark
        receipt_date = row.receipt_date
        receipt_amt = row.receipt_amt
    if commitment_date:
        frappe.db.set_value('Sales Invoice', doc.name,
                            'commitment_date', commitment_date, update_modified=False)
    if commitment_amt:
        frappe.db.set_value('Sales Invoice', doc.name,
                            'commitment_amt', commitment_amt, update_modified=False)
    if remark:
        frappe.db.set_value('Sales Invoice', doc.name,
                            'remark', remark, update_modified=False)
    if receipt_date:
        frappe.db.set_value('Sales Invoice', doc.name,
                            'receipt_date', receipt_date, update_modified=False)
    if receipt_amt:
        frappe.db.set_value('Sales Invoice', doc.name,
                            'receipt_amt', receipt_amt, update_modified=False)


def validate_delivery_item(doc, method):
    from pni_customization.utility.delivery_note import validate
    validate(doc, method)
    data = []
    for row in doc.pni_packing_table:
        if row.pni_carton in data:
            frappe.throw("Duplicate Carton Entry {0}".format(row.pni_carton))
        else:
            data.append(row.pni_carton)
    for item in doc.items:
        if item.is_paper_plate or item.paper_cup:
            if not(item.base_uom_rate > 0):
                frappe.throw(
                    "Paper Cup and Plate Rate can't be zero for " + item.item_code)
            item.rate = float(item.base_uom_rate) * \
                float(item.conversion_factor)


def update_pni_gate_entry(doc, method):
    if doc.pni_gate_entry:
        ge = frappe.get_doc("PNI Gate Entry", doc.pni_gate_entry)
        # on_submit on_cancel
        if ge.docstatus != 1 and method == "on_submit":
            frappe.throw("Gate Entry Not SUbmited Yet")
        if ge.entry_status == "Delivered" and method == "on_submit":
            frappe.throw("This Gate Entry Already Delivered")
        if method == "on_submit":
            ge.entry_status = "Delivered"
        else:
            ge.entry_status = "Pending For Delivery"
        ge.save(ignore_permissions=True)


@frappe.whitelist()
def submit_delivery_item(doc, method):
    items_calc = {}
    for row in doc.pni_packing_table:

        weight = items_calc.get(row.item, 0)
        items_calc.update({row.item: (weight + float(row.total_qty))})

        if row.packing_type == "PNI Carton":
            carton = frappe.get_doc("PNI Carton", row.pni_carton)

            validate_pni_packing(row.pni_carton, carton.item,
                                 carton.warehouse, doc.items, doc.is_return)

            if not doc.is_return:
                carton.status = "Delivered"
            else:
                carton.status = "Available"
                carton.warehouse = get_carton_warehouse(carton.item, doc.items)
                carton.is_return = True

            if carton.docstatus != 1:
                frappe.throw("Carton Not SUbmitted")

            carton.save()

        if row.packing_type == "PNI Bag":
            bag = frappe.get_doc("PNI Bag", row.pni_carton)

            validate_pni_packing(row.pni_carton, bag.item,
                                 bag.warehouse, doc.items, doc.is_return)

            if not doc.is_return:
                bag.status = "Sold"
            else:
                bag.status = "In Stock"
                bag.warehouse = get_carton_warehouse(bag.item, doc.items)
                bag.is_return = True

            if bag.docstatus != 1:
                frappe.throw("Bag Not SUbmitted")

            bag.save()

        if row.packing_type == "Reel":
            reel = frappe.get_doc("Reel", row.pni_carton)

            validate_pni_packing(row.pni_carton, reel.item,
                                 reel.warehouse, doc.items, doc.is_return)

            if not doc.is_return:
                reel.status = "Sold"
            else:
                reel.status = "In Stock"
                reel.warehouse = get_carton_warehouse(reel.item, doc.items)
                reel.is_return = True

            if reel.docstatus != 1:
                frappe.throw("Reel Not SUbmitted")

            reel.save()
    item_in_table = {}
    for item in doc.items:
        weight = item_in_table.get(item.item_code, 0)
        item_in_table.update(
            {item.item_code: (weight + float(item.stock_qty))})
    for data in items_calc:
        if item_in_table.get(data) and items_calc.get(data):
            if round(item_in_table.get(data), 2) != round(items_calc.get(data), 2) and not doc.is_return:
                frappe.throw("{0}'s qty({1}) is not metch in item table qty({2})".format(
                    data, round(item_in_table.get(data), 2), round(items_calc.get(data), 2)))


def get_carton_warehouse(packing_item, items):
    for item in items:
        if packing_item == item.item_code:
            return item.warehouse


def validate_pni_packing(pni_carton, packing_item, packing_item_warehouse, items, is_return=False):
    item_exist = False
    for item in items:
        if packing_item == item.item_code:
            item_exist = True
            if packing_item_warehouse != item.warehouse and not is_return:
                frappe.throw("Packing {0}'s warehouse {1} not match with Delivery Item's Warehouse: {2}".format(
                    pni_carton, packing_item_warehouse, item.warehouse))
    if not item_exist:
        frappe.throw("Packing {0}'s item {1} not available in Delivery Item".format(
            pni_carton, packing_item))


@frappe.whitelist()
def cancel_delivery_item(doc, method):
    for row in doc.pni_packing_table:
        if row.packing_type == "PNI Carton":
            carton = frappe.get_doc("PNI Carton", row.pni_carton)
            if doc.is_return:
                carton.status = "Delivered"
            else:
                carton.status = "Available"
            carton.save()
        if row.packing_type == "PNI Bag":
            bag = frappe.get_doc("PNI Bag", row.pni_carton)
            if doc.is_return:
                bag.status = "Sold"
            else:
                bag.status = "In Stock"
            bag.save()
        if row.packing_type == "Reel":
            reel = frappe.get_doc("Reel", row.pni_carton)
            if doc.is_return:
                reel.status = "Sold"
            else:
                reel.status = "In Stock"
            reel.save()


@frappe.whitelist()
def submit_work_order_item(doc, method):
    pass


@frappe.whitelist()
def validate_inspection_for_work_order(doc, method):
    if doc.work_order and doc.stock_entry_type == "Manufacture":
        wo = frappe.get_doc("Work Order", doc.work_order)
        if wo and not wo.skip_pni_quality_inspection:
            qty_stock = 0
            qty_stock += int(doc.fg_completed_qty)

            # Get qty from submited stock entry
            stock_entrys = frappe.get_all("Stock Entry", {
                "work_order": doc.work_order,
                "stock_entry_type": "Manufacture",
                "docstatus": 1
            })
            for se in stock_entrys:
                se_doc = frappe.get_doc("Stock Entry", se.name)
                qty_stock += int(se_doc.fg_completed_qty)

            pni_qi = frappe.get_all("PNI Quality Inspection", {
                                    "reference_name": wo.name, "docstatus": 1})
            inspect_qty = 0
            for qi in pni_qi:
                pni_qi_doc = frappe.get_doc("PNI Quality Inspection", qi.name)
                inspect_qty += int(pni_qi_doc.total_qty)
            if inspect_qty < qty_stock:
                frappe.throw(" Please do PNI Quality Inspection for {0} Items".format(
                    str(qty_stock - inspect_qty)))


@frappe.whitelist()
def validate_work_order_item(doc, method):
    update_work_order(doc.name)
    check_stock(doc)
    if doc.required_items:
        if doc.bom_no:
            bom = frappe.get_doc("BOM", doc.bom_no)
            for row in doc.required_items:
                if not row.source_warehouse:
                    frappe.throw(
                        "Source Warehouse needed on Row {0}".format(row.idx))
                if not row.pni_qty_per_piece:
                    for bom_item in bom.items:
                        if bom_item.item_code == row.item_code:
                            row.pni_qty_per_piece = bom_item.pni_qty_per_piece


def check_stock(doc):
    doc.stock_short = False
    for row in doc.required_items:
        if not row.available_qty_at_source_warehouse:
            row.available_qty_at_source_warehouse = 0
        if float(row.required_qty) > float(row.available_qty_at_source_warehouse):
            doc.stock_short = True
    if doc.get('workflow_state') and doc.workflow_state == "Pending For Material Issue" and doc.stock_short and (not doc.skip_short_stock):
        frappe.throw(
            "Couldn't Pending For Material Issue because stock shortage")


def on_update_after_submit_work_order_item(doc, method):
    check_stock(doc)


def update_work_order_state():
    wos_short_closed = frappe.get_all('Work Order', filters=[
        ["status", "not in", "Stopped,Completed"],
        ["short_closed", "=", True]
    ], fields=['name'])
    for wo in wos_short_closed:
        frappe.db.set_value("Work Order", wo.name, "short_closed", False)
    frappe.db.commit()
    wos = frappe.get_all('Work Order', filters=[
        ["workflow_state", "=", "Pending For Material Issue"],
        ["material_transferred_for_manufacturing", ">", "0"]
    ], fields=['name'])
    for wo in wos:
        frappe.db.set_value("Work Order", wo.name,
                            "workflow_state", "In Process")
        print(wo.name)
    frappe.db.commit()

    _wos = frappe.get_all('Work Order', filters=[
        ["workflow_state", "!=", "Completed"],
        ["status", "=", "Completed"]
    ], fields=['name'])
    for wo in _wos:
        frappe.db.set_value("Work Order", wo.name,
                            "workflow_state", "Completed")
        print(wo.name)
    frappe.db.commit()


@frappe.whitelist()
def validate_stock_entry_item(doc, method):
    if doc.purpose == "Send to Warehouse" and (doc.pni_reference_type not in ["Customer", "Supplier"]):
        frappe.throw(
            "For Purpose Send to Warehouse PNI Reference Type must be Customer/Supplier")
    if doc.purpose == "Send to Warehouse" and not doc.pni_reference_type:
        frappe.throw(
            "For Purpose Send to Warehouse PNI Reference is Mandatory")
    if doc.scrap_entry and not doc.pni_shift:
        frappe.throw("Shift is Mandatory for Scrap Entry")
    if doc.scrap_entry and not doc.pni_reference:
        frappe.throw("Workstation is Mandatory for Scrap Entry")
    validate_repack_entry(doc)
    validate_inspection_for_work_order(doc, method)
    if doc.items:
        if doc.bom_no:
            bom = frappe.get_doc("BOM", doc.bom_no)
            if bom:
                for row in doc.items:
                    if not row.pni_qty_per_piece:
                        for bom_item in bom.items:
                            if bom_item.item_code == row.item_code:
                                row.pni_qty_per_piece = bom_item.pni_qty_per_piece


@frappe.whitelist()
def get_outstanding_invoice(customer):
    data = frappe.get_list("Sales Invoice",
                           fields=["name", "posting_date", "customer",
                                   "rounded_total", "outstanding_amount"],
                           filters={"docstatus": 1, "customer": customer,
                                    "outstanding_amount": (">", 0)}
                           )
    total = 0
    for row in data:
        total += row.outstanding_amount
    return {"data": data, "total": total}


def submit_repack_entry(stock_entry, method):
    if stock_entry.stock_entry_type == "Repack" and stock_entry.packing_type == "PNI Carton":
        for item in stock_entry.pni_carton_in:
            carton = frappe.get_doc("PNI Carton", item.pni_carton)
            if(method == "on_submit"):
                carton.status = "Repack"
            else:
                carton.status = "Available"
            carton.save()
        for item in stock_entry.pni_packing_carton:
            carton = frappe.get_doc("PNI Carton", item.carton_id)
            if(method == "on_submit"):
                carton.status = "Available"
                carton.save()
                carton.submit()
            else:
                carton.cancel()


def validate_repack_entry(stock_entry):
    if stock_entry.stock_entry_type == "Repack" and stock_entry.packing_type == "PNI Carton":
        setting = frappe.get_doc("PNI Settings", "PNI Settings")
        # if not self.carton_weight:
        # 	self.carton_weight = setting.paper_cup_carton_weight
        for data in stock_entry.pni_packing_carton:
            if data.weight:
                data.net_weight = float(data.weight) - \
                    float(data.carton_weight)
            if not data.carton_id:
                doc = frappe.get_doc({
                    "doctype": "PNI Carton",
                    "naming_series": setting.paper_plate_carton_series if stock_entry.is_paper_plate else setting.paper_cup_carton_series,
                    "item": stock_entry.carton_item,
                    "posting_date": stock_entry.posting_date
                })
                doc.insert()
                data.carton_id = doc.name
            if data.carton_id:
                doc2 = frappe.get_doc("PNI Carton", data.carton_id)
                doc2.is_paper_plate = True if stock_entry.is_paper_plate else False
                doc2.posting_date = stock_entry.posting_date
                doc2.item = stock_entry.carton_item
                doc2.shift = stock_entry.shift
                doc2.supervisor = stock_entry.supervisor
                doc2.supervisor_name = stock_entry.supervisor_name
                doc2.item_name = frappe.get_value(
                    "Item", stock_entry.carton_item, "item_name")
                doc2.item_description = frappe.get_value(
                    "Item", stock_entry.carton_item, "description")
                doc2.gross_weight = data.weight
                doc2.net_weight = data.net_weight
                doc2.total = float(
                    stock_entry.conversation_factor if stock_entry.conversation_factor else 0)
                doc2.warehouse = stock_entry.carton_warehouse
                doc2.save()
    if stock_entry.stock_entry_type == "Repack" and stock_entry.packing_type == "PNI Bag":
        pass


@frappe.whitelist()
def job_card_submit(doc, method):
    total_qty = 0
    for item in doc.time_logs:
        total_qty += item.completed_qty
    pni_qi = frappe.get_all("PNI Quality Inspection", {
                            "reference_name": doc.name, "pre_pni_inspection": False, "docstatus": 1})
    inspect_qty = 0
    for qi in pni_qi:
        pni_qi_doc = frappe.get_doc("PNI Quality Inspection", qi.name)
        inspect_qty += int(pni_qi_doc.accepted_qty)
    if inspect_qty < total_qty and not doc.skip_pni_quality_inspection:
        frappe.throw(" Please do PNI QUality Inspection for {0} Items".format(
            str(total_qty - inspect_qty)))


@frappe.whitelist()
def job_card_update(doc, method):
    operation = frappe.get_doc("Operation", doc.operation)
    if operation and operation.pre_pni_inspection and doc.job_started:
        total_qty = 0
        for item in doc.time_logs:
            total_qty += item.completed_qty
        pni_qi = frappe.get_all("PNI Quality Inspection", {
                                "reference_name": doc.name, "pre_pni_inspection": True, "docstatus": 1})
        print(total_qty)
        inspect_qty = 0
        for qi in pni_qi:
            pni_qi_doc = frappe.get_doc("PNI Quality Inspection", qi.name)
            inspect_qty += int(pni_qi_doc.accepted_qty)
        if inspect_qty == 0 and not doc.skip_pni_quality_inspection:
            frappe.throw(" Pre PNI Quality Inpection Needed")
        if inspect_qty < total_qty and not doc.skip_pni_quality_inspection:
            frappe.throw(" Please do Pre PNI QUality Inspection for {0} Items".format(
                str(total_qty - inspect_qty)))


@frappe.whitelist()
def job_card_onload(doc, method):
    data = frappe.db.sql("""select sum(jctl.completed_qty) from `tabJob Card Time Log` jctl
			INNER JOIN
				`tabJob Card` jc
			on jc.name = jctl.parent
			where jc.work_order = %s and jc.operation = %s and jc.docstatus <> 2""", (doc.work_order, doc.operation))
    if data and data[0] and data[0][0]:
        wo = frappe.get_doc("Work Order", doc.work_order)
        doc.pni_balance_qty = int(wo.qty) - int(data[0][0])
    # doc.save()


def validate_opportunity(doc, method):
    if doc.status == "Closed" or doc.status == "Lost":
        if not doc.pni_attachment:
            frappe.throw(
                "Close or Lost Opportunity  must have PNI Attachments!")


def validate_items(se_items, co_items):
    # validate for items not in coating item
    for se_item in se_items:
        if not filter(lambda x: x == se_item.item_code, co_items):
            frappe.throw(_("Item {0} - {1} cannot be part of this Stock Entry").format(
                se_item.item_code, se_item.item_name))


def validate_se_qty_coating(se, co):
    validate_material_qty_coating(se.items, co.coating_table)
    validate_ldpe_qty_coating(se.items, co.ldpe_bag)
    validate_scrap_qty_coating(se.items, co.coating_scrap)


def validate_ldpe_qty_coating(se_items, co_items):
    # TODO allow multiple raw material transfer?
    for material in co_items:
        qty = 0
        for item in se_items:
            if(material.reel_in == item.item_code):
                qty += item.qty
        if(qty != material.weight):
            frappe.throw(_("Total quantity of Item {0} - {1} should be {2}"
                           ).format(material.item, material.item, material.quantity))


def validate_material_qty_coating(se_items, co_items):
    # TODO allow multiple raw material transfer?
    for material in co_items:
        qty = 0
        for item in se_items:
            if(material.item == item.item_code):
                qty += item.qty
        if(qty != material.quantity):
            frappe.throw(_("Total quantity of Item {0} - {1} should be {2}"
                           ).format(material.item, material.item, material.quantity))


def validate_scrap_qty_coating(se_items, co_items):
    # TODO allow multiple raw material transfer?
    for material in co_items:
        qty = 0
        for item in se_items:
            if(material.item == item.item_code):
                qty += item.qty
        if(qty != material.quantity):
            frappe.throw(_("Total quantity of Item {0} - {1} should be {2}"
                           ).format(material.item, material.item, material.quantity))


def manage_se_submit(se, co):
    if co.docstatus == 0:
        frappe.throw(_("Submit the  {0} {1} to make Stock Entries").format(
            co.doctype, co.name))

    if co.status in ["Completed", "Cancelled"]:
        frappe.throw(
            "You cannot make entries against Completed/Cancelled Process Orders")
    co.status = "Completed"
    co.flags.ignore_validate_update_after_submit = True
    co.save()


def manage_se_cancel(se, co):
    if(co.status == "Completed"):
        try:
            # validate_material_qty_coating(se.items, co.coating_table)
            co.status = "Pending For Stock Entry"
        except:
            frappe.throw("Please cancel the production stock entry first.")
    else:
        frappe.throw("Process order status must be Completed")
    co.flags.ignore_validate_update_after_submit = True
    co.save()


def validate_po(doc, method):
    validate_purchase_order(doc)
    item_array_mr, item_array_po = {}, {}
    doc.same_price_purchase = True
    total_qty, received_qty = 0.0, 0.0

    for item in doc.items:
        is_stock_item = frappe.get_cached_value(
            'Item', item.item_code, 'is_stock_item')
        is_fixed_asset = frappe.get_cached_value(
            'Item', item.item_code, 'is_fixed_asset')
        if not is_stock_item and not is_fixed_asset:
            item.received_qty = item.qty
        received_qty += item.received_qty
        total_qty += item.qty
        if item.material_request:
            check_mr_qty(doc, item.material_request, item.item_code, item.qty)
        if round(item.last_purchase_rate, 4) < round(item.rate, 4):
            doc.same_price_purchase = False
        if item.material_request:
            mr = frappe.get_doc("Material Request", item.material_request)
            for mr_item in mr.items:
                if mr_item.item_code == item.item_code:
                    if item.qty > mr_item.qty:
                        frappe.throw("Purchase Order {0}({1}) Qty should not greater then Material Request {2}({3})".format(
                            item.item_code,
                            item.qty,
                            mr_item.item_code,
                            mr_item.qty
                        ))
    if total_qty:
        doc.db_set("per_received", flt(received_qty/total_qty)
                   * 100, update_modified=False)
    else:
        doc.db_set("per_received", 0, update_modified=False)

    # Validation for field phone, email and party_gstin in supplier
    if doc.supplier:
        supplier = frappe.get_doc('Supplier', doc.supplier)
        contact = frappe.db.sql(""" select email_id, phone, gstin from `tabAddress`
			where name in
			(select parent from `tabDynamic Link` where link_doctype = 'Supplier' and link_name = %s
			and parenttype = 'Address')""", doc.supplier, as_dict=1)
        # print(contact[0])
        if contact:
            if not contact[0].email_id:
                frappe.throw("Supplier Email Id is not available")
            if not contact[0].phone:
                frappe.throw("Supplier phone number is not available")
            if not contact[0].gstin:
                frappe.throw("Supplier must have GSTIN number")


def check_mr_qty(po, mr, item_code, qty):
    pos = frappe.get_all(
        "Purchase Order Item",
        filters={
            "item_code": item_code,
            "docstatus": ('!=', '2'),
            "material_request": mr
        },
        fields=['qty', 'parent']
    )
    total_qty = qty
    if pos:
        for item in pos:
            if item['parent'] == po.name:
                continue
            total_qty += item['qty']
    mr_obj = frappe.get_doc("Material Request", mr)
    mr_qty = 0
    for item in mr_obj.items:
        if item.item_code == item_code:
            mr_qty += item.qty
    if total_qty > mr_qty:
        frappe.throw("""Purchase Order Total Qty {0} for Item {1} is greater then Material Request {2}
			Qty {3}
		""".format(total_qty, item_code, mr, mr_qty))


@frappe.whitelist()
def manage_se_changes(doc, method):
    update_pni_gate_entry(doc, method)
    submit_repack_entry(doc, method)
    if doc.pni_reference and doc.pni_reference_type == "PNI Packing":
        co = frappe.get_doc("PNI Packing", doc.pni_reference)
        if(method == "on_submit"):

            co_items = []
            co_items.append(co.item)

            validate_items(doc.items, co_items)

            manage_se_submit(doc, co)
        elif(method == "on_cancel"):
            manage_se_cancel(doc, co)

    if doc.pni_reference and doc.pni_reference_type == "Coating":
        co = frappe.get_doc("Coating", doc.pni_reference)
        if(method == "on_submit"):

            co_items = []
            for item in co.coating_table:
                reel_in = frappe.get_doc("Reel", item.reel_in)
                reel_out = frappe.get_doc("Reel", item.reel_out)
                co_items.append(reel_in.item)
                co_items.append(reel_out.item)
            for item in co.coating_scrap:
                co_items.append(item.item)
            if co.ldpe_bag > 0:
                paper_blank_setting = frappe.get_doc(
                    "Paper Blank Settings", "Paper Blank Settings")
                co_items.append(paper_blank_setting.ldpe_bag)

            validate_items(doc.items, co_items)

            # validate_se_qty_coating(doc, co)
            # frappe.throw("Success")
            manage_se_submit(doc, co)
        elif(method == "on_cancel"):
            manage_se_cancel(doc, co)

    if doc.pni_reference and doc.pni_reference_type == "Slitting":
        slitting = frappe.get_doc("Slitting", doc.pni_reference)
        if(method == "on_submit"):

            slitting_items = []
            for item in slitting.slitting_table:
                reel_in = frappe.get_doc("Reel", item.reel_in)
                if item.type != "Bottom Reel":
                    reel_out = frappe.get_doc("Reel", item.reel_out)
                slitting_items.append(reel_in.item)
                if item.type != "Bottom Reel":
                    slitting_items.append(reel_out.item)
                else:
                    slitting_items.append(item.item_out)
            for item in slitting.slitting_scrap:
                slitting_items.append(item.item)

            validate_items(doc.items, slitting_items)

            # validate_se_qty_coating(doc, co)
            # frappe.throw("Success")
            manage_se_submit(doc, slitting)
        elif(method == "on_cancel"):
            manage_se_cancel(doc, slitting)

    if doc.pni_reference and doc.pni_reference_type == "Printing":
        printing = frappe.get_doc("Printing", doc.pni_reference)
        if(method == "on_submit"):

            printing_items = []
            for item in printing.printing_table:
                reel_in = frappe.get_doc("Reel", item.reel_in)
                if not item.merge_reel:
                    reel_out = frappe.get_doc("Reel", item.reel_out)
                printing_items.append(reel_in.item)
                printing_items.append(reel_out.item)
            for item in printing.printing_scrap:
                printing_items.append(item.item)
            for item in printing.printing_inc_table:
                printing_items.append(item.item)

            validate_items(doc.items, printing_items)

            # validate_se_qty_coating(doc, co)
            # frappe.throw("Success")
            manage_se_submit(doc, printing)
        elif(method == "on_cancel"):
            manage_se_cancel(doc, printing)

    if doc.pni_reference and doc.pni_reference_type == "Punching":
        punching = frappe.get_doc("Punching", doc.pni_reference)
        if(method == "on_submit"):

            punching_items = []
            for item in punching.punching_table:
                reel_in = frappe.get_doc("Reel", item.reel_in)
                if not item.half_reel:
                    punch_table = frappe.get_doc(
                        "Punch Table", item.punch_table)
                    punching_items.append(punch_table.item)
                punching_items.append(reel_in.item)

            for item in punching.punching_scrap:
                punching_items.append(item.item)

            validate_items(doc.items, punching_items)

            # validate_se_qty_coating(doc, co)
            # frappe.throw("Success")
            manage_se_submit(doc, punching)
        elif(method == "on_cancel"):
            manage_se_cancel(doc, punching)

    if doc.pni_reference and doc.pni_reference_type == "Packing":
        Packing = frappe.get_doc("Packing", doc.pni_reference)
        if(method == "on_submit"):

            packing_items = []
            packing_items.append(Packing.item)
            packing_items.append(Packing.bag_item)
            for item in Packing.packing_scrap:
                packing_items.append(item.item)

            validate_items(doc.items, packing_items)

            # validate_se_qty_coating(doc, co)
            # frappe.throw("Success")
            manage_se_submit(doc, Packing)
        elif(method == "on_cancel"):
            manage_se_cancel(doc, Packing)

    if doc.pni_reference and doc.pni_reference_type == "PNI Material Transfer":
        Packing = frappe.get_doc("PNI Material Transfer", doc.pni_reference)
        if(method == "on_submit"):

            packing_items = []
            packing_items.append(Packing.item)

            validate_items(doc.items, packing_items)

            # validate_se_qty_coating(doc, co)
            # frappe.throw("Success")
            manage_se_submit(doc, Packing)
        elif(method == "on_cancel"):
            manage_se_cancel(doc, Packing)


@frappe.whitelist()
def get_attributes():
    return ["abc", "def"]


@frappe.whitelist(allow_guest=True)
def create_lead(name, prefix="", leadid="", leadtype="", mobile="",
                phone="", email="", date="", category="",
                city="", area="", brancharea="", dncmobile="",
                dncphone="", company="", pincode="", time="", branchpin="", parentid=""):
    """
            Create lead from Out Side
    """
    lead = frappe.get_doc({
        "doctype": "Lead",
        "lead_name": prefix + " " + name,
        "j_leadid": leadid,
        "j_leadtype": leadtype,
        "mobile_no": mobile,
        "phone": phone,
        "j_email": email,
        "j_date": date,
        "j_category": category,
        "j_city": city,
        "j_area": area,
        "j_brancharea": brancharea,
        "j_dncmobile": dncmobile,
        "j_dncphone": dncphone,
        "j_company": company,
        "j_pincode": pincode,
        "j_time": time,
        "j_branchpin": branchpin,
        "j_parentid": parentid,
        "source": "Just Dial"
    })
    lead.insert(ignore_permissions=True)
    frappe.db.commit()
    return lead.name
