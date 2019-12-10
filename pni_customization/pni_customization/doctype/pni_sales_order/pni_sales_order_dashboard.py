from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'pni_sales_order',
		'non_standard_fieldnames': {
		},
		'internal_links': {
			
		},
		'transactions': [
			{
				'label': _('Accounts'),
				'items': ['Payment Entry', 'Delivery Note']
			}
		]
	}