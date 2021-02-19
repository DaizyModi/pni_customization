from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        'heatmap': True,
        'heatmap_message': _('This is based on transaction against the Purchase Executive. See timeline below for details'),
        'fieldname': 'purchase_executive',
        'transactions': [
            {
                'label': _('Purchase'),
                'items': ['Purchase Order', 'Purchase Invoice', 'Purchase Receipt']
            },
        ]

    }
