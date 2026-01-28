# -*- coding: utf-8 -*-
{
    'name': 'AI Assistant',
    'version': '15.0.2.0.0',
    'category': 'Productivity',
    'summary': 'AI Assistant với giao diện Chat hiện đại và phân tích thông minh',
    'description': """
        Module AI Assistant tích hợp với OpenRouter API
        ================================================
        
        Tính năng:
        - Hỗ trợ AI cho Nhân sự: Đánh giá nhân viên, gợi ý đào tạo
        - Hỗ trợ AI cho Dự án: Phân tích rủi ro, ước tính timeline
        - Hỗ trợ AI cho Công việc: Ước tính thời gian, gợi ý phân công
        - Chat với AI Assistant
    """,
    'author': 'FITDNU',
    'website': 'https://fitdnu.edu.vn',
    'depends': ['base', 'mail', 'nhan_su', 'quan_ly_du_an', 'quan_ly_cong_viec'],
    'data': [
        'security/ir.model.access.csv',
        'data/ai_config_data.xml',
        'views/ai_config_views.xml',
        'views/ai_chat_views.xml',
        'wizards/ai_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ai_assistant/static/src/css/ai_chat.css',
            'ai_assistant/static/src/css/ai_wizard.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
