{
    'name': 'Project Management',
    'version': '15.0.1.0',
    'category': 'Project',
    'summary': 'Project Management Module',
    'description': """
        Project Management Module for FitDNU
    """,
    'author': 'FitDNU',
    'website': 'https://fitdnu.edu.vn',
    'depends': ['project', 'hr', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
