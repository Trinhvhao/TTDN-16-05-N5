# -*- coding: utf-8 -*-
{
    'name': 'Quản Lý Dự Án',
    'version': '15.0.1.0.0',
    'summary': 'Module quản lý dự án tích hợp với nhân sự',
    'description': """
        Module Quản Lý Dự Án
        ====================
        - Quản lý thông tin dự án
        - Theo dõi tiến độ dự án
        - Quản lý ngân sách dự án
        - Tích hợp với module Nhân sự và Quản lý công việc
        
        Được phát triển và sửa đổi bởi Trịnh Văn Hào, nhóm 5
    """,
    'author': 'TTDN-15-03-N7',
    'category': 'Project Management',
    'depends': ['base', 'mail', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'data/du_an_data.xml',
        'views/du_an_moc_views.xml',
        'views/du_an_cap_nhat_views.xml',
        'views/du_an_views.xml',
        'views/nhan_su_extend_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
