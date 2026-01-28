# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class AIChat(models.Model):
    _name = 'ai.chat'
    _description = 'Lịch sử chat với AI'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Tiêu đề', compute='_compute_name', store=True)
    user_id = fields.Many2one('res.users', string='Người dùng', default=lambda self: self.env.user)
    
    # Liên kết với các model
    res_model = fields.Char(string='Model liên quan')
    res_id = fields.Integer(string='ID bản ghi')
    
    message_ids = fields.One2many('ai.chat.message', 'chat_id', string='Tin nhắn')
    
    # Thống kê
    message_count = fields.Integer(string='Số tin nhắn', compute='_compute_message_count', store=True)
    
    # Input field for new message
    new_message = fields.Text(string='Tin nhắn mới')
    
    @api.depends('message_ids')
    def _compute_name(self):
        for record in self:
            if record.message_ids:
                first_msg = record.message_ids.filtered(lambda m: m.role == 'user')
                if first_msg:
                    record.name = first_msg[0].content[:50] + '...' if len(first_msg[0].content) > 50 else first_msg[0].content
                else:
                    record.name = f'Chat {record.id}'
            else:
                record.name = f'Chat mới'

    @api.depends('message_ids')
    def _compute_message_count(self):
        for record in self:
            record.message_count = len(record.message_ids)

    def action_send_message(self):
        """Gửi tin nhắn từ input box"""
        self.ensure_one()
        if not self.new_message or not self.new_message.strip():
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'message': 'Vui lòng nhập nội dung tin nhắn!', 'type': 'warning'}}
        
        try:
            # Gửi và nhận phản hồi
            self.send_message(self.new_message)
            # Xóa input
            self.new_message = False
            
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'message': '✅ Đã gửi tin nhắn thành công!', 'type': 'success'}}
        except Exception as e:
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'message': f'Lỗi: {str(e)}', 'type': 'danger'}}

    def send_message(self, content, context_data=None):
        """Gửi tin nhắn và nhận phản hồi từ AI"""
        self.ensure_one()
        
        # Lưu tin nhắn người dùng
        self.env['ai.chat.message'].create({
            'chat_id': self.id,
            'role': 'user',
            'content': content
        })
        
        # Lấy cấu hình AI
        config = self.env['ai.config'].get_default_config()
        
        # Xây dựng lịch sử chat
        history = []
        for msg in self.message_ids.sorted('create_date'):
            history.append({
                'role': msg.role,
                'content': msg.content
            })
        
        # Thêm tin nhắn mới
        history.append({
            'role': 'user',
            'content': content
        })
        
        # Gọi AI
        try:
            response = config.call_ai(content, context_data=context_data)
            
            # Lưu phản hồi AI
            self.env['ai.chat.message'].create({
                'chat_id': self.id,
                'role': 'assistant',
                'content': response
            })
            
            return response
        except Exception as e:
            # Lưu lỗi
            self.env['ai.chat.message'].create({
                'chat_id': self.id,
                'role': 'assistant',
                'content': f'Lỗi: {str(e)}',
                'is_error': True
            })
            raise


class AIChatMessage(models.Model):
    _name = 'ai.chat.message'
    _description = 'Tin nhắn chat AI'
    _order = 'create_date asc'

    chat_id = fields.Many2one('ai.chat', string='Phiên chat', required=True, ondelete='cascade')
    role = fields.Selection([
        ('user', 'Người dùng'),
        ('assistant', 'AI'),
        ('system', 'Hệ thống')
    ], string='Vai trò', required=True)
    content = fields.Text(string='Nội dung', required=True)
    is_error = fields.Boolean(string='Là lỗi', default=False)
    
    # Timestamps
    create_date = fields.Datetime(string='Thời gian')
