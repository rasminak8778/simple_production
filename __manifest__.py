{
    'name': 'Simple Production',
    'version': '17.0.1.0.0',
    'description': 'Manufacturing of simple product',
    'category': 'Purchase/Simple Production',
    'summary': 'Product Manufacturing',
    'installable': True,
    'application': True,
    'depends': [
        'base',
        'purchase',
        ],
    'data': [
        'security/ir.model.access.csv',
        'data/manufacture_location_data.xml',
        'views/product_template_views.xml',
        'views/bom_views.xml',
        # 'views/bom_new_line_views.xml',
        'views/manufacturing_views.xml',
        'views/stock_move_views.xml',
        'views/product_menu.xml',
    ]
}