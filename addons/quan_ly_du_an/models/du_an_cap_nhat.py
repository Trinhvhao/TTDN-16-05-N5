# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta

STATUS_COLOR = {
    'on_track': 20,      # green / success
    'at_risk': 2,        # orange
    'off_track': 23,     # red / danger
    'on_hold': 4,        # light blue
    False: 0,            # default grey
}


class DuAnCapNhat(models.Model):
    _name = 'du_an.cap_nhat'
    _description = 'Cập nhật tiến độ dự án'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'ngay_cap_nhat desc, id desc'

    # ==================== THÔNG TIN CƠ BẢN ====================
    name = fields.Char(string='Tiêu đề', required=True, tracking=True)
    du_an_id = fields.Many2one(
        'du_an',
        string='Dự án',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    # ==================== TRẠNG THÁI ====================
    status = fields.Selection([
        ('on_track', 'Đúng tiến độ'),
        ('at_risk', 'Có rủi ro'),
        ('off_track', 'Chậm tiến độ'),
        ('on_hold', 'Tạm dừng')
    ], string='Trạng thái', required=True, default='on_track', tracking=True)
    
    color = fields.Integer(
        string='Color Index',
        compute='_compute_color',
        store=True
    )
    
    # ==================== TIẾN ĐỘ ====================
    progress = fields.Integer(
        string='Tiến độ (%)',
        default=0,
        tracking=True,
        help='Tiến độ hoàn thành dự án (0-100)'
    )
    
    progress_percentage = fields.Float(
        string='Tiến độ (Decimal)',
        compute='_compute_progress_percentage',
        store=True
    )
    
    # ==================== THỜI GIAN & NGƯỜI CẬP NHẬT ====================
    ngay_cap_nhat = fields.Date(
        string='Ngày cập nhật',
        default=fields.Date.context_today,
        required=True,
        tracking=True
    )
    
    nguoi_cap_nhat_id = fields.Many2one(
        'res.users',
        string='Người cập nhật',
        default=lambda self: self.env.user,
        required=True
    )
    
    # ==================== NỘI DUNG CẬP NHẬT ====================
    noi_dung = fields.Html(
        string='Nội dung cập nhật',
        help='Báo cáo chi tiết về tiến độ, công việc đã làm'
    )
    
    cong_viec_da_hoan_thanh = fields.Text(
        string='Công việc đã hoàn thành',
        help='Liệt kê các công việc đã hoàn thành trong kỳ'
    )
    
    cong_viec_dang_thuc_hien = fields.Text(
        string='Công việc đang thực hiện',
        help='Các công việc đang trong quá trình thực hiện'
    )
    
    ke_hoach_tuan_toi = fields.Text(
        string='Kế hoạch tuần/tháng tới',
        help='Kế hoạch công việc cho giai đoạn tiếp theo'
    )
    
    # ==================== VẤN ĐỀ & RỦI RO ====================
    van_de = fields.Text(
        string='Vấn đề gặp phải',
        help='Các vấn đề, trở ngại đang gặp phải'
    )
    
    giai_phap = fields.Text(
        string='Giải pháp đề xuất',
        help='Các giải pháp để xử lý vấn đề'
    )
    
    rui_ro_moi = fields.Text(
        string='Rủi ro mới phát sinh',
        help='Các rủi ro mới được phát hiện'
    )
    
    # ==================== NGÂN SÁCH ====================
    ngan_sach_da_su_dung = fields.Float(
        string='Ngân sách đã sử dụng',
        help='Tổng ngân sách đã chi tiêu đến thời điểm cập nhật'
    )
    
    ngan_sach_du_kien_con_lai = fields.Float(
        string='Ngân sách còn lại dự kiến',
        compute='_compute_ngan_sach_con_lai',
        store=True
    )
    
    # ==================== MILESTONE ====================
    milestones_reached = fields.Many2many(
        'du_an.moc',
        'du_an_cap_nhat_moc_rel',
        'cap_nhat_id',
        'moc_id',
        string='Mốc đã đạt được',
        help='Các milestone đã hoàn thành trong kỳ báo cáo này'
    )
    
    # ==================== KHÁC ====================
    name_cropped = fields.Char(
        string='Tiêu đề rút gọn',
        compute='_compute_name_cropped'
    )
    
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'du_an_cap_nhat_attachment_rel',
        'cap_nhat_id',
        'attachment_id',
        string='Tài liệu đính kèm'
    )
    
    tag_ids = fields.Many2many(
        'du_an.cap_nhat.tag',
        string='Tags'
    )

    # ==================== COMPUTED FIELDS ====================
    @api.depends('status')
    def _compute_color(self):
        """Tính màu hiển thị dựa trên status"""
        for record in self:
            record.color = STATUS_COLOR.get(record.status, 0)

    @api.depends('progress')
    def _compute_progress_percentage(self):
        """Chuyển đổi progress sang dạng decimal"""
        for record in self:
            record.progress_percentage = record.progress / 100.0

    @api.depends('name')
    def _compute_name_cropped(self):
        """Rút gọn tên nếu quá dài"""
        for record in self:
            if record.name:
                record.name_cropped = (record.name[:57] + '...') if len(record.name) > 60 else record.name
            else:
                record.name_cropped = ''

    @api.depends('ngan_sach_da_su_dung', 'du_an_id.ngan_sach_du_kien')
    def _compute_ngan_sach_con_lai(self):
        """Tính ngân sách còn lại"""
        for record in self:
            if record.du_an_id and record.du_an_id.ngan_sach_du_kien:
                record.ngan_sach_du_kien_con_lai = record.du_an_id.ngan_sach_du_kien - record.ngan_sach_da_su_dung
            else:
                record.ngan_sach_du_kien_con_lai = 0.0

    # ==================== ORM OVERRIDE ====================
    @api.model
    def create(self, vals):
        """Khi tạo update mới, cập nhật last_update cho dự án"""
        update = super(DuAnCapNhat, self).create(vals)
        
        # Cập nhật tiến độ cho dự án
        if update.du_an_id and 'progress' in vals:
            update.du_an_id.sudo().write({
                'tien_do': vals['progress'],
                'last_update_id': update.id,
                'last_update_status': vals.get('status', 'on_track')
            })
        
        return update

    def write(self, vals):
        """Khi cập nhật, đồng bộ tiến độ với dự án"""
        res = super(DuAnCapNhat, self).write(vals)
        
        # Cập nhật tiến độ cho dự án nếu có thay đổi
        if 'progress' in vals or 'status' in vals:
            for record in self:
                if record.du_an_id:
                    update_vals = {}
                    if 'progress' in vals:
                        update_vals['tien_do'] = vals['progress']
                    if 'status' in vals:
                        update_vals['last_update_status'] = vals['status']
                    
                    if update_vals:
                        record.du_an_id.sudo().write(update_vals)
        
        return res

    def unlink(self):
        """Khi xóa update, cập nhật lại last_update của dự án"""
        du_an_ids = self.mapped('du_an_id')
        res = super(DuAnCapNhat, self).unlink()
        
        for du_an in du_an_ids:
            last_update = self.search(
                [('du_an_id', '=', du_an.id)],
                order='ngay_cap_nhat desc, id desc',
                limit=1
            )
            if last_update:
                du_an.sudo().write({
                    'last_update_id': last_update.id,
                    'last_update_status': last_update.status
                })
        
        return res

    # ==================== ACTIONS ====================
    def action_view_du_an(self):
        """Xem chi tiết dự án"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dự án',
            'res_model': 'du_an',
            'res_id': self.du_an_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # ==================== HELPER METHODS ====================
    @api.model
    def _build_description_template(self, du_an):
        """Tạo template mô tả tự động cho update"""
        milestones = self.env['du_an.moc'].search([
            ('du_an_id', '=', du_an.id),
            ('deadline', '>=', fields.Date.today() - timedelta(days=30)),
            ('deadline', '<=', fields.Date.today() + timedelta(days=30))
        ])
        
        template = f"""
        <h3>Cập nhật tiến độ dự án: {du_an.ten_du_an}</h3>
        <p><strong>Ngày cập nhật:</strong> {fields.Date.today()}</p>
        <p><strong>Tiến độ hiện tại:</strong> {du_an.tien_do}%</p>
        
        <h4>Các mốc quan trọng:</h4>
        <ul>
        """
        
        for milestone in milestones:
            status_icon = '✅' if milestone.is_reached else '⏳'
            template += f"<li>{status_icon} {milestone.name} - Deadline: {milestone.deadline}</li>"
        
        template += "</ul>"
        
        return template


class DuAnCapNhatTag(models.Model):
    _name = 'du_an.cap_nhat.tag'
    _description = 'Tag cho cập nhật dự án'

    name = fields.Char(string='Tên tag', required=True)
    color = fields.Integer(string='Color Index')
