# Docs: https://www.odoo.com/documentation/20.0/developer/reference/backend/module.html
#  - 'name' is the only required key; 'version' should follow semantic versioning
#  - 'depends': modules loaded BEFORE this one (we alter/use project.* resources)
#  - 'data': files always loaded at install/update, paths relative to module root
#  - 'external_dependencies': python/bin dependencies
# Docs (load order): https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/04_securityintro.html
#  - data files are loaded sequentially in manifest order: if A refers to B, B goes first
{
    'name': 'Taskmaster',
    'version': '20.0.1.0.0',
    'summary': 'AI risk-management agent for Project (kanban + task form)',
    'category': 'Services/Project',
    'author': 'Taskmaster team',
    'license': 'LGPL-3',
    'depends': ['project'],
    'data': [
        # security first: Odoo 20 uses security/ir.access.csv (model ir.access), not ir.model.access.csv
        'security/ir.access.csv',
        # wizard view + action BEFORE the views that reference the action
        'wizard/taskmaster_risk_wizard_views.xml',
        'views/project_task_views.xml',
    ],
    'external_dependencies': {'python': ['requests']},
    'assets': {
        'web.assets_backend': [
            'taskmaster/static/src/js/risk_wizard.js',
        ],
    },
    'application': False,
    'installable': True,
}
