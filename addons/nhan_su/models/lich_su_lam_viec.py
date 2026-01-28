# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class LichSuLamViec(models.Model):
    _name = 'lich_su_lam_viec'
    _description = 'Bảng chứa thông tin lịch sử làm việc'
    _order = 'ngay_bat_dau desc'

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True,
        ondelete='cascade'
    )
    phong_ban_id = fields.Many2one(
        'phong_ban',
        string='Phòng ban',
        required=True
    )
    chuc_vu_id = fields.Many2one(
        'chuc_vu',
        string='Chức vụ'
    )
    
    ngay_bat_dau = fields.Date(string='Ngày bắt đầu', required=True)
    ngay_ket_thuc = fields.Date(string='Ngày kết thúc')
    
    ly_do_thay_doi = fields.Text(string='Lý do thay đổi')
    ghi_chu = fields.Text(string='Ghi chú')
    
    trang_thai = fields.Selection([
        ('dang_lam', 'Đang làm việc'),
        ('da_chuyen', 'Đã chuyển'),
        ('nghi_viec', 'Nghỉ việc')
    ], string='Trạng thái', default='dang_lam')

    thoi_gian_lam_viec = fields.Integer(
        string='Thời gian làm việc (ngày)',
        compute='_compute_thoi_gian_lam_viec',
        store=True
    )

    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_thoi_gian_lam_viec(self):
        for record in self:
            if record.ngay_bat_dau:
                end_date = record.ngay_ket_thuc or date.today()
                record.thoi_gian_lam_viec = (end_date - record.ngay_bat_dau).days
            else:
                record.thoi_gian_lam_viec = 0

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.nhan_vien_id.ho_ten} - {record.phong_ban_id.ten_phong_ban}"
            result.append((record.id, name))
        return result