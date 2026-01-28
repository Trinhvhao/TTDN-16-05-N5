# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class AIQuickAskWizard(models.TransientModel):
    _name = 'ai.quick.ask.wizard'
    _description = 'Hỏi nhanh AI'

    question = fields.Text(string='Câu hỏi')
    answer = fields.Text(string='Trả lời', readonly=True)
    
    # Template questions
    template_question = fields.Selection([
        ('custom', 'Câu hỏi tùy chỉnh'),
        ('summary', 'Tóm tắt thông tin này'),
        ('analyze', 'Phân tích điểm mạnh/yếu'),
        ('improve', 'Gợi ý cải thiện'),
        ('risk', 'Đánh giá rủi ro'),
        ('timeline', 'Ước tính thời gian'),
        ('recommend', 'Khuyến nghị hành động'),
    ], string='Mẫu câu hỏi', default='custom')
    
    # Context
    context_model = fields.Char(string='Model')
    context_id = fields.Integer(string='Record ID')
    context_info = fields.Text(string='Thông tin ngữ cảnh', readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        
        # Lấy context từ active record
        if self.env.context.get('active_model') and self.env.context.get('active_id'):
            model = self.env.context['active_model']
            record_id = self.env.context['active_id']
            
            res['context_model'] = model
            res['context_id'] = record_id
            
            # Lấy thông tin ngữ cảnh
            record = self.env[model].browse(record_id)
            if hasattr(record, 'name'):
                res['context_info'] = f"Model: {model}\nRecord: {record.name}"
            elif hasattr(record, 'ten_du_an'):
                res['context_info'] = f"Dự án: {record.ten_du_an}"
            elif hasattr(record, 'ten_cong_viec'):
                res['context_info'] = f"Công việc: {record.ten_cong_viec}"
            elif hasattr(record, 'ho_ten'):
                res['context_info'] = f"Nhân viên: {record.ho_ten}"
        
        return res

    @api.onchange('template_question')
    def _onchange_template_question(self):
        """Tự động điền câu hỏi theo template"""
        if self.template_question and self.template_question != 'custom':
            templates = {
                'summary': 'Hãy tóm tắt thông tin quan trọng về bản ghi này.',
                'analyze': 'Phân tích điểm mạnh và điểm yếu của bản ghi này.',
                'improve': 'Đề xuất những cách cải thiện và tối ưu hóa.',
                'risk': 'Đánh giá các rủi ro tiềm ẩn và biện pháp phòng ngừa.',
                'timeline': 'Ước tính timeline và các mốc thời gian quan trọng.',
                'recommend': 'Khuyến nghị hành động cụ thể cần thực hiện tiếp theo.',
            }
            self.question = templates.get(self.template_question, '')

    def action_ask(self):
        """Gửi câu hỏi đến AI"""
        self.ensure_one()
        
        if not self.question:
            raise UserError('Vui lòng nhập câu hỏi!')
        
        config = self.env['ai.config'].get_default_config()
        
        # Xây dựng context
        context_data = None
        if self.context_model and self.context_id:
            record = self.env[self.context_model].browse(self.context_id)
            if record.exists():
                context_data = self._get_record_data(record)
        
        try:
            result = config.call_ai(self.question, context_data=context_data)
            self.answer = result
            
            # Trả về wizard để hiển thị kết quả
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ai.quick.ask.wizard',
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }
        except Exception as e:
            raise UserError(str(e))

    def _get_record_data(self, record):
        """Lấy dữ liệu từ record để gửi cho AI"""
        data = {}
        
        if hasattr(record, 'ho_ten'):  # Nhân viên
            data = {
                'type': 'nhan_vien',
                'ho_ten': record.ho_ten,
                'chuc_vu': record.chuc_vu_id.name if record.chuc_vu_id else '',
                'phong_ban': record.phong_ban_id.ten_phong_ban if record.phong_ban_id else '',
            }
        elif hasattr(record, 'ten_du_an'):  # Dự án
            data = {
                'type': 'du_an',
                'ten_du_an': record.ten_du_an,
                'trang_thai': record.trang_thai,
                'tien_do': record.tien_do,
            }
        elif hasattr(record, 'ten_cong_viec'):  # Công việc
            data = {
                'type': 'cong_viec',
                'ten_cong_viec': record.ten_cong_viec,
                'trang_thai': record.trang_thai,
                'tien_do': record.tien_do,
            }
        
        return data


class AIAnalysisWizard(models.TransientModel):
    _name = 'ai.analysis.wizard'
    _description = 'Phân tích AI'

    analysis_type = fields.Selection([
        ('nhan_vien', 'Phân tích nhân viên'),
        ('du_an', 'Phân tích dự án'),
        ('cong_viec', 'Phân tích công việc'),
        ('tong_hop', 'Phân tích tổng hợp'),
    ], string='Loại phân tích', required=True, default='tong_hop')
    
    date_from = fields.Date(string='Từ ngày')
    date_to = fields.Date(string='Đến ngày')
    
    result = fields.Html(string='Kết quả phân tích', readonly=True)

    def action_save_to_chat(self):
        """Lưu kết quả phân tích vào chat history"""
        self.ensure_one()
        if not self.result:
            raise UserError('Chưa có kết quả để lưu!')
        
        # Tạo chat mới
        chat = self.env['ai.chat'].create({
            'name': f'Phân tích {dict(self._fields["analysis_type"].selection)[self.analysis_type]}'
        })
        
        # Lưu prompt
        prompt_text = f"Phân tích {dict(self._fields['analysis_type'].selection)[self.analysis_type]}"
        if self.date_from:
            prompt_text += f" từ {self.date_from}"
        if self.date_to:
            prompt_text += f" đến {self.date_to}"
        
        self.env['ai.chat.message'].create({
            'chat_id': chat.id,
            'role': 'user',
            'content': prompt_text
        })
        
        # Lưu kết quả
        self.env['ai.chat.message'].create({
            'chat_id': chat.id,
            'role': 'assistant',
            'content': self.result
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ai.chat',
            'res_id': chat.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_analyze(self):
        """Thực hiện phân tích"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        data = {}
        
        if self.analysis_type == 'nhan_vien':
            # Thống kê nhân viên
            nhan_vien = self.env['nhan_vien'].search([('active', '=', True)])
            data = {
                'tong_nhan_vien': len(nhan_vien),
                'theo_trang_thai': {},
                'theo_phong_ban': {},
            }
            for nv in nhan_vien:
                # Theo trạng thái
                tt = nv.trang_thai
                data['theo_trang_thai'][tt] = data['theo_trang_thai'].get(tt, 0) + 1
                # Theo phòng ban
                pb = nv.phong_ban_id.ten_phong_ban if nv.phong_ban_id else 'Chưa phân'
                data['theo_phong_ban'][pb] = data['theo_phong_ban'].get(pb, 0) + 1
                
        elif self.analysis_type == 'du_an':
            # Thống kê dự án
            du_an = self.env['du_an'].search([('active', '=', True)])
            data = {
                'tong_du_an': len(du_an),
                'theo_trang_thai': {},
                'tong_ngan_sach': sum(du_an.mapped('ngan_sach_du_kien')),
                'tong_chi_phi': sum(du_an.mapped('ngan_sach_thuc_te')),
                'tre_tien_do': len(du_an.filtered('tre_tien_do')),
            }
            for da in du_an:
                tt = da.trang_thai
                data['theo_trang_thai'][tt] = data['theo_trang_thai'].get(tt, 0) + 1
                
        elif self.analysis_type == 'cong_viec':
            # Thống kê công việc
            cong_viec = self.env['cong_viec'].search([('active', '=', True)])
            data = {
                'tong_cong_viec': len(cong_viec),
                'theo_trang_thai': {},
                'tre_han': len(cong_viec.filtered('tre_han')),
                'tong_gio_uoc_tinh': sum(cong_viec.mapped('thoi_gian_uoc_tinh')),
                'tong_gio_thuc_te': sum(cong_viec.mapped('thoi_gian_thuc_te')),
            }
            for cv in cong_viec:
                tt = cv.trang_thai_id.name if cv.trang_thai_id else 'Chưa phân loại'
                data['theo_trang_thai'][tt] = data['theo_trang_thai'].get(tt, 0) + 1
                
        else:  # Tổng hợp
            nhan_vien = self.env['nhan_vien'].search([('active', '=', True)])
            du_an = self.env['du_an'].search([('active', '=', True)])
            cong_viec = self.env['cong_viec'].search([('active', '=', True)])
            
            data = {
                'nhan_su': {
                    'tong': len(nhan_vien),
                    'dang_lam': len(nhan_vien.filtered(lambda x: x.trang_thai == 'dang_lam')),
                },
                'du_an': {
                    'tong': len(du_an),
                    'dang_thuc_hien': len(du_an.filtered(lambda x: x.trang_thai == 'dang_thuc_hien')),
                    'hoan_thanh': len(du_an.filtered(lambda x: x.trang_thai == 'hoan_thanh')),
                    'tre_tien_do': len(du_an.filtered('tre_tien_do')),
                },
                'cong_viec': {
                    'tong': len(cong_viec),
                    'hoan_thanh': len(cong_viec.filtered(lambda x: x.stage_type == 'done')),
                    'dang_lam': len(cong_viec.filtered(lambda x: x.stage_type == 'in_progress')),
                    'tre_han': len(cong_viec.filtered('tre_han')),
                }
            }
        
        import json
        prompt = f"""Phân tích dữ liệu sau và đưa ra nhận xét chi tiết:
1. Tình hình tổng quan
2. Điểm mạnh
3. Vấn đề cần chú ý  
4. Đề xuất cải thiện
5. Dự báo và khuyến nghị

Hãy trả lời bằng HTML đẹp với các heading, list và strong tags.

Dữ liệu:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            self.result = result
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ai.analysis.wizard',
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }
        except Exception as e:
            raise UserError(str(e))
