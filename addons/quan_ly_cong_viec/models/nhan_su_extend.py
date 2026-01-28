# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NhanVienExtend(models.Model):
    """Extend nhan_vien model to add task relationships"""
    _inherit = 'nhan_vien'
    
    # Quan hệ với công việc
    cong_viec_ids = fields.One2many(
        'cong_viec',
        'nguoi_phu_trach_id',
        string='Công việc được giao'
    )
    
    # Số công việc được giao
    so_cong_viec = fields.Integer(
        string='Số công việc',
        compute='_compute_so_cong_viec',
        store=True
    )
    
    @api.depends('cong_viec_ids')
    def _compute_so_cong_viec(self):
        for record in self:
            record.so_cong_viec = len(record.cong_viec_ids)


class DuAnExtend(models.Model):
    """Extend du_an model to add task relationships"""
    _inherit = 'du_an'
    
    # Quan hệ với công việc
    cong_viec_ids = fields.One2many(
        'cong_viec',
        'du_an_id',
        string='Danh sách công việc'
    )
    
    so_cong_viec = fields.Integer(
        string='Số công việc',
        compute='_compute_thong_ke_cong_viec',
        store=True
    )
    
    so_cong_viec_hoan_thanh = fields.Integer(
        string='Công việc hoàn thành',
        compute='_compute_thong_ke_cong_viec',
        store=True
    )
    
    so_cong_viec_dang_lam = fields.Integer(
        string='Công việc đang làm',
        compute='_compute_thong_ke_cong_viec',
        store=True
    )
    
    # Override tiến độ và ngân sách để tính từ công việc
    tien_do = fields.Float(
        string='Tiến độ (%)',
        compute='_compute_tien_do',
        store=True,
        help='Tiến độ hoàn thành dự án dựa trên các công việc'
    )
    
    ngan_sach_thuc_te = fields.Float(
        string='Ngân sách thực tế',
        compute='_compute_ngan_sach_thuc_te',
        store=True
    )

    @api.depends('cong_viec_ids', 'cong_viec_ids.trang_thai_id', 'cong_viec_ids.trang_thai_id.stage_type')
    def _compute_thong_ke_cong_viec(self):
        for record in self:
            cong_viecs = record.cong_viec_ids
            record.so_cong_viec = len(cong_viecs)
            record.so_cong_viec_hoan_thanh = len(cong_viecs.filtered(lambda x: x.trang_thai_id.stage_type == 'done'))
            record.so_cong_viec_dang_lam = len(cong_viecs.filtered(lambda x: x.trang_thai_id.stage_type == 'in_progress'))

    @api.depends('cong_viec_ids', 'cong_viec_ids.tien_do')
    def _compute_tien_do(self):
        for record in self:
            if record.cong_viec_ids:
                total_progress = sum(record.cong_viec_ids.mapped('tien_do'))
                record.tien_do = total_progress / len(record.cong_viec_ids)
            else:
                record.tien_do = 0.0

    @api.depends('cong_viec_ids', 'cong_viec_ids.chi_phi')
    def _compute_ngan_sach_thuc_te(self):
        for record in self:
            record.ngan_sach_thuc_te = sum(record.cong_viec_ids.mapped('chi_phi'))

    def action_view_cong_viec(self):
        """Mở danh sách công việc của dự án"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Công việc - {self.ten_du_an}',
            'res_model': 'cong_viec',
            'view_mode': 'kanban,tree,form',
            'domain': [('du_an_id', '=', self.id)],
            'context': {
                'default_du_an_id': self.id,
            }
        }

