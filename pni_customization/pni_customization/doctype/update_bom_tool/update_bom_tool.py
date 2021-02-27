# -*- coding: utf-8 -*-
# Copyright (c) 2021, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class UpdateBOMTool(Document):
    def get_bom(self):
        bom_list = frappe.get_all("BOM", {'is_active': 1, 'is_default': 1})
        if bom_list:
            for boms in bom_list:
                if boms:
                    bom = boms['name']
                    self.check_bom_is_active_default(bom)
                else:
                    return None
        else:
            return None

    def get_new_bom(self):
        if self.default_active_bom_list:
            for row in self.get('default_active_bom_list'):
                if row.old_bom:
                    self.get_default_active_bom(row)
                else:
                    return None
        else:
            frappe.throw("No Old BOM found in List")

    def check_bom_is_active_default(self, bom):
        """
                Check if current bom is active and also is default
        """
        bom_obj = frappe.get_doc("BOM", bom)
        if bom_obj.is_active and bom_obj.is_default:
            if bom_obj.items:
                for row in bom_obj.get('items'):
                    if row.bom_no:
                        self.check_bom_is_active_default(row.bom_no)
                    else:
                        return None
            else:
                return None
        else:
            row = self.append('default_active_bom_list', {})
            row.old_bom = bom_obj.name
            self.save()
            frappe.db.commit()
        self.set("default_active_bom_list", [])

    def get_default_active_bom(self, row):
        bom_obj = frappe.get_doc("BOM", row.old_bom)
        if bom_obj:
            new_bom_obj = frappe.get_all("BOM", filters={
                'item': bom_obj.item,
                'docstatus': True,
                'is_active': True,
                'is_default': True
            }, fields=['name'])
            if new_bom_obj:
                row.new_bom = new_bom_obj[0].name
                self.save()
                frappe.db.commit()
            else:
                return None
        else:
            frappe.throw("No new BOM found")

    def replace_bom(self):
        if self.default_active_bom_list:
            list_for_bom = {}
            for row in self.get('default_active_bom_list'):
                list_for_bom[row.old_bom] = row.new_bom
            frappe.enqueue("pni_customization.utility.bom_utility.enqueue_bom_processing",
                           _args=list_for_bom, timeout=90000)
            self.set("default_active_bom_list", [])
            self.save()
            frappe.db.commit()
        else:
            frappe.throw("Get Old and New BOMs First")
