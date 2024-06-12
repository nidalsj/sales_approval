{
    'name': 'Sales Approval',
    'category': 'Sales',
    'summary': 'Inventory Lot Management',
    'license': 'LGPL-3',
    'depends':['base','stock','sale'],
    'version': '1.0',
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'views/sale_order_views.xml',
    ],


    'installable': True,
    'auto_install': False,
    'application': False,
}
