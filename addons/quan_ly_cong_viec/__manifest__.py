# -*- coding: utf-8 -*-
{
    'name': 'Quản Lý Công Việc',
    'version': '15.0.1.0.0',
    'summary': 'Module quản lý công việc - chia nhỏ dự án thành các task',
    'description': """
        Module Quản Lý Công Việc
        ========================
        - Quản lý công việc/tác vụ của dự án
        - Chia nhỏ dự án thành các task để theo dõi sát sao
        - Gán người phụ trách, thời gian và trạng thái
        - Theo dõi tiến độ và hiệu suất từng cá nhân
        - Tích hợp với module Nhân sự và Quản lý dự án
        
        Tính năng chính:
        - Tạo và quản lý công việc
        - Liên kết công việc với dự án
        - Gán người phụ trách (từ module Nhân sự)
        - Theo dõi thời gian bắt đầu - kết thúc
        - Cập nhật trạng thái công việc
        - Báo cáo tiến độ và hiệu suất cá nhân
        
        Được phát triển và sửa đổi bởi Trịnh Văn Hào, nhóm 5
    """,
    'author': 'TTDN-15-03-N7',
    'category': 'Project Management',
    'depends': ['base', 'mail', 'nhan_su', 'quan_ly_du_an'],
    'data': [
        'security/ir.model.access.csv',
        'data/cong_viec_stage_data.xml',
        'data/cong_viec_data.xml',
        'data/cong_viec_cron.xml',
        'data/demo_data.xml',
        'views/cong_viec_trang_thai_views.xml',
        'views/cong_viec_views.xml',
        'views/hieu_suat_views.xml',
        'views/nhan_vien_extend_views.xml',
        'views/du_an_extend_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'quan_ly_cong_viec/static/src/css/kanban_colorful.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
