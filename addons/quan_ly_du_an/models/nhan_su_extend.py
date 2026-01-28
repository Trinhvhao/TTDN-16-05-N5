# -*- coding: utf-8 -*-
from odoo import models, fields


class NhanVienExtend(models.Model):
    """Extend nhan_vien model to add project relationships"""
    _inherit = 'nhan_vien'
    
    # Quan hệ với dự án (tham gia dự án)
    du_an_ids = fields.Many2many(
        'du_an',
        'du_an_nhan_vien_rel',
        'nhan_vien_id',
        'du_an_id',
        string='Dự án tham gia'
    )


class PhongBanExtend(models.Model):
    """Extend phong_ban model to add project relationships"""
    _inherit = 'phong_ban'
    
    # Quan hệ với dự án
    du_an_ids = fields.One2many(
        'du_an',
        'phong_ban_id',
        string='Dự án'
    )
