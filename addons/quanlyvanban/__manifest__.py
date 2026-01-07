# -*- coding: utf-8 -*-
{
    'name': "Quản lý văn bản",
    'summary': "Quản lý văn bản và kết nối với nhân sự",
    'description': """
        Module quản lý văn bản với các tính năng:
        - 
        - Quản lý văn bản với số hiệu, nơi gửi đến
        - Kết nối với nhân viên xử lý
        - Theo dõi trạng thái xử lý
    """,
    'author': "Trinh Hao",
    'website': "http://www.yourcompany.com",
    'category': 'Document Management',
    'version': '1.0',
    'depends': ['base', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/loai_van_ban.xml',
        'views/van_ban.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
