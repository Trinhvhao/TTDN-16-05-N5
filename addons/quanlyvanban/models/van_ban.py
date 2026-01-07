# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VanBan(models.Model):
    _name = 'van_ban'
    _description = 'Văn bản'
    _rec_name = 'so_hieu_van_ban'
    _order = "ngay_tao desc"
    
    # Thông tin cơ bản
    so_hieu_van_ban = fields.Char("Số hiệu văn bản", required=True)
    ten_van_ban = fields.Char("Tên văn bản", required=True)
    ngay_tao = fields.Date("Ngày tạo", required=True, default=fields.Date.today)
    loai_van_ban_id = fields.Many2one('loai_van_ban', string="Loại văn bản", required=True)
    
    # Nơi gửi đến
    noi_gui_den = fields.Text("Nơi gửi đến", help="Các phòng ban/cá nhân nhận văn bản")
    
    # Nhân sự xử lý (kết nối với module nhân sự)
    nhan_su_xu_li_id = fields.Many2one(
        'nhan_vien',
        string="Nhân sự xử lý",
        required=True,
        help="Nhân viên chịu trách nhiệm xử lý văn bản"
    )
    phong_ban_id = fields.Many2one(
        'phong_ban',
        string="Phòng ban xử lý",
        related='nhan_su_xu_li_id.phong_ban_id',
        store=True,
        readonly=True
    )
    
    # Nội dung và trạng thái
    noi_dung = fields.Text("Nội dung văn bản")
    mo_ta = fields.Text("Mô tả")
    han_xu_ly = fields.Date("Hạn xử lý")
    
    trang_thai = fields.Selection([
        ('new', 'Mới tạo'),
        ('processing', 'Đang xử lý'),
        ('approved', 'Đã phê duyệt'),
        ('completed', 'Hoàn tất'),
        ('rejected', 'Từ chối'),
    ], string="Trạng thái", default='new', required=True)
    
    # Kết quả
    ket_qua_xu_ly = fields.Text("Kết quả xử lý")
    ngay_hoan_tat = fields.Date("Ngày hoàn tất")
    
    # Người tạo
    nguoi_tao = fields.Many2one(
        'res.users',
        string="Người tạo",
        readonly=True,
        default=lambda self: self.env.user
    )
    
    @api.constrains('so_hieu_van_ban')
    def _check_unique_so_hieu_van_ban(self):
        for record in self:
            if record.so_hieu_van_ban and self.search_count([
                ('so_hieu_van_ban', '=', record.so_hieu_van_ban),
                ('id', '!=', record.id)
            ]):
                raise ValidationError(f"Số hiệu văn bản '{record.so_hieu_van_ban}' đã tồn tại!")
    
    @api.constrains('han_xu_ly', 'ngay_tao')
    def _check_han_xu_ly(self):
        for record in self:
            if record.han_xu_ly and record.ngay_tao:
                if record.han_xu_ly < record.ngay_tao:
                    raise ValidationError("Hạn xử lý phải sau ngày tạo!")
    
    def action_gui_duyet(self):
        """Gửi văn bản để duyệt"""
        self.write({'trang_thai': 'processing'})
    
    def action_phe_duyet(self):
        """Phê duyệt văn bản"""
        self.write({'trang_thai': 'approved'})
    
    def action_tu_choi(self):
        """Từ chối văn bản"""
        self.write({'trang_thai': 'rejected'})
    
    def action_hoan_tat(self):
        """Hoàn tất xử lý"""
        self.write({
            'trang_thai': 'completed',
            'ngay_hoan_tat': fields.Date.today()
        })
