{
    'name': 'Real Estate',
    'version': '16.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Shlimazes first module',
    'website': 'https://www.odoo.com/app/real_estate',
    'depends': [
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml'
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
