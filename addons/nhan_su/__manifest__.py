# -*- coding: utf-8 -*-
{
    'name': 'Quản Lý Nhân Sự',
    'version': '15.0.1.0.0',
    'summary': 'Module quản lý thông tin nhân viên, phòng ban, chức vụ',
    'description': """
        Module Quản Lý Nhân Sự
        =======================
        - Quản lý thông tin nhân viên
        - Quản lý phòng ban, chức vụ
        - Lịch sử làm việc
        - Tích hợp với các module quản lý dự án và công việc
        
        Được phát triển và sửa đổi bởi Trịnh Văn Hào, nhóm 5
    """,
    'author': 'TTDN-15-03-N7',
    'category': 'Human Resources',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/nhan_su_data.xml',
        'views/nhan_vien_views.xml',
        'views/phong_ban_views.xml',
        'views/chuc_vu_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
