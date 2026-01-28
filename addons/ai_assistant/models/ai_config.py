# -*- coding: utf-8 -*-
import requests
import json
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AIConfig(models.Model):
    _name = 'ai.config'
    _description = 'Cấu hình AI'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Tên cấu hình', required=True, default='OpenRouter API')
    api_key = fields.Char(string='API Key', required=True)
    api_url = fields.Char(
        string='API URL',
        default='https://openrouter.ai/api/v1/chat/completions'
    )
    model = fields.Char(
        string='Model',
        default='xiaomi/mimo-v2-flash:free'
    )
    max_tokens = fields.Integer(string='Max Tokens', default=2048)
    temperature = fields.Float(string='Temperature', default=0.7)
    active = fields.Boolean(default=True, string='Hoạt động')
    
    # Prompts mặc định
    system_prompt = fields.Text(
        string='System Prompt',
        default="""Bạn là AI Assistant chuyên nghiệp hỗ trợ quản lý doanh nghiệp. 
Bạn có thể giúp:
- Đánh giá và phân tích nhân viên
- Lập kế hoạch dự án và ước tính rủi ro
- Phân công và ước tính công việc
- Đưa ra các gợi ý tối ưu hóa quy trình

Hãy trả lời bằng tiếng Việt, ngắn gọn và chuyên nghiệp."""
    )

    @api.model
    def get_default_config(self):
        """Lấy cấu hình AI mặc định"""
        config = self.search([('active', '=', True)], limit=1)
        if not config:
            _logger.warning("⚠️ Chưa cấu hình AI. Vui lòng vào menu Cấu hình > Cấu hình hệ thống > AI Config để thiết lập API Key của bạn.")
            raise UserError("""
            Chưa cấu hình AI!
            
            Vui lòng:
            1. Vào menu Cấu hình > Cấu hình hệ thống > AI Config
            2. Nhập API Key của OpenRouter (lấy tại https://openrouter.ai)
            3. Lưu cấu hình
            
            Sau đó quay lại và thử lại.
            """)
        return config

    def call_ai(self, prompt, system_prompt=None, context_data=None):
        """
        Gọi AI API
        :param prompt: Câu hỏi/yêu cầu
        :param system_prompt: System prompt (nếu không có sẽ dùng mặc định)
        :param context_data: Dữ liệu ngữ cảnh bổ sung
        :return: Kết quả từ AI
        """
        self.ensure_one()
        
        if not self.api_key:
            raise UserError('Chưa cấu hình API Key!')
        
        # Xây dựng messages
        messages = []
        
        # System prompt
        sys_prompt = system_prompt or self.system_prompt
        if context_data:
            sys_prompt += f"\n\nThông tin ngữ cảnh:\n{json.dumps(context_data, ensure_ascii=False, indent=2)}"
        
        messages.append({
            "role": "system",
            "content": sys_prompt
        })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Gọi API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://odoo.local",
            "X-Title": "Odoo AI Assistant"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                raise UserError(f'Lỗi từ AI API: Không có kết quả trả về')
                
        except requests.exceptions.Timeout:
            raise UserError('Timeout khi gọi AI API. Vui lòng thử lại.')
        except requests.exceptions.RequestException as e:
            _logger.error(f'AI API Error: {str(e)}')
            raise UserError(f'Lỗi khi gọi AI API: {str(e)}')
        except Exception as e:
            _logger.error(f'Unexpected AI Error: {str(e)}')
            raise UserError(f'Lỗi không xác định: {str(e)}')

    def test_connection(self):
        """Test kết nối API"""
        self.ensure_one()
        try:
            result = self.call_ai("Xin chào! Hãy trả lời ngắn gọn để test kết nối.")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': f'Kết nối AI thành công! Phản hồi: {result[:100]}...',
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Lỗi!',
                    'message': str(e),
                    'type': 'danger',
                    'sticky': True,
                }
            }
