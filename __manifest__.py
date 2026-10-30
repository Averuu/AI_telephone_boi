{
    'name': 'Taskmaster',
    'version': '20.0.1.0.0',
    'category': 'Services/Project',
    'summary': 'Taskmaster example description',
    'author': 'Оверфиттим под заказчика',
    'depends': ['project'],
    'data': [
        'security/ir.access.csv',
        'views/task_wizard_views.xml',
        'views/project_views_inherit.xml',
    ],
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
