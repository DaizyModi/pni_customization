from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'pni_material_request',
		'non_standard_fieldnames': {
			
		},
		'internal_links': {
		},
		'transactions': [
			{
				'label': _('Fulfillment'),
				'items': ['Stock Entry']
			}
		]
	}