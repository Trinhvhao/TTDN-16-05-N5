# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Chức vụ của nhân viên'
    _rec_name = 'ten_chuc_vu'

    ma_chuc_vu = fields.Char(
        string='Mã chức vụ',
        required=True,
        copy=False
    )
    ten_chuc_vu = fields.Char(string='Tên chức vụ', required=True)
    cap_bac = fields.Integer(string='Cấp bậc', default=1, help='Cấp bậc chức vụ (1 là thấp nhất)')
    mo_ta = fields.Text(string='Mô tả')
    
    # Quan hệ One2many với nhân viên
    nhan_vien_ids = fields.One2many(
        'nhan_vien',
        'chuc_vu_id',
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
            name = f"[{record.ma_chuc_vu}] {record.ten_chuc_vu}" if record.ma_chuc_vu else record.ten_chuc_vu
            result.append((record.id, name))
        return result

    _sql_constraints = [
        ('ma_chuc_vu_unique', 'UNIQUE(ma_chuc_vu)', 'Mã chức vụ phải là duy nhất!')
    ]