import frappe


def validate(mr, method):
    for raw in mr.items:
        if not check_item_workflow_state(raw.item_code):
            frappe.throw("{0} Invalid Item ".format(raw.item_code))


def check_item_workflow_state(item):
    state = frappe.get_value("Item", item, "workflow_state")
    if state not in ["Checked", "Approved", "Old Item"]:
        return False
    else:
        True
