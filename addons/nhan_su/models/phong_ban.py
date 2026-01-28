# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Phòng ban của nhân viên'
    _rec_name = 'ten_phong_ban'

    ma_phong_ban = fields.Char(
        string='Mã phòng ban',
        required=True,
        copy=False
    )
    ten_phong_ban = fields.Char(string='Tên phòng ban', required=True)
    mo_ta = fields.Text(string='Mô tả')
    
    # Trưởng phòng
    truong_phong_id = fields.Many2one(
        'nhan_vien',
        string='Trưởng phòng'
    )
    
    # Quan hệ One2many với nhân viên
    nhan_vien_ids = fields.One2many(
        'nhan_vien',
        'phong_ban_id',
        string='Danh sách nhân viên'
    )
    
    so_nhan_vien = fields.Integer(
        string='Số nhân viên',
        compute='_compute_so_nhan_vien',
        store=True
    )
    
    active = fields.Boolean(default=True, string='Hoạt động')

    @api.depends('nhan_vien_ids')
    def _compute_so_nhan_vien(self):
        for record in self:
            record.so_nhan_vien = len(record.nhan_vien_ids)

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.ma_phong_ban}] {record.ten_phong_ban}" if record.ma_phong_ban else record.ten_phong_ban
            result.append((record.id, name))
        return result

    _sql_constraints = [
        ('ma_phong_ban_unique', 'UNIQUE(ma_phong_ban)', 'Mã phòng ban phải là duy nhất!')
    ]