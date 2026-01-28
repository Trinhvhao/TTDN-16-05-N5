# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HieuSuatNhanVien(models.Model):
    _name = 'hieu_suat.nhan_vien'
    _description = 'Báo cáo hiệu suất nhân viên'
    _auto = False  # Đây là model SQL view, không tạo bảng thực
    _rec_name = 'nhan_vien_id'
    _order = 'ty_le_hoan_thanh desc'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', readonly=True)
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', readonly=True)
    
    tong_cong_viec = fields.Integer(string='Tổng công việc', readonly=True)
    cong_viec_hoan_thanh = fields.Integer(string='Hoàn thành', readonly=True)
    cong_viec_dang_lam = fields.Integer(string='Đang làm', readonly=True)
    cong_viec_chua_lam = fields.Integer(string='Chưa làm', readonly=True)
    cong_viec_tre_han = fields.Integer(string='Trễ hạn', readonly=True)
    
    ty_le_hoan_thanh = fields.Float(string='Tỷ lệ hoàn thành (%)', readonly=True)
    ty_le_dung_han = fields.Float(string='Tỷ lệ đúng hạn (%)', readonly=True)
    
    tien_do_trung_binh = fields.Float(string='Tiến độ TB (%)', readonly=True)
    thoi_gian_uoc_tinh_tong = fields.Float(string='TG ước tính (giờ)', readonly=True)
    thoi_gian_thuc_te_tong = fields.Float(string='TG thực tế (giờ)', readonly=True)

    def init(self):
        """Tạo SQL view cho báo cáo hiệu suất"""
        self.env.cr.execute("""
            DROP VIEW IF EXISTS hieu_suat_nhan_vien;
            CREATE OR REPLACE VIEW hieu_suat_nhan_vien AS (
                SELECT
                    ROW_NUMBER() OVER (ORDER BY nv.id) as id,
                    nv.id as nhan_vien_id,
                    nv.phong_ban_id as phong_ban_id,
                    COUNT(cv.id) as tong_cong_viec,
                    COUNT(CASE WHEN cvt.stage_type = 'done' THEN 1 END) as cong_viec_hoan_thanh,
                    COUNT(CASE WHEN cvt.stage_type = 'in_progress' THEN 1 END) as cong_viec_dang_lam,
                    COUNT(CASE WHEN cvt.stage_type = 'new' THEN 1 END) as cong_viec_chua_lam,
                    COUNT(CASE WHEN cv.tre_han = true THEN 1 END) as cong_viec_tre_han,
                    CASE 
                        WHEN COUNT(cv.id) > 0 THEN 
                            ROUND(COUNT(CASE WHEN cvt.stage_type = 'done' THEN 1 END) * 100.0 / COUNT(cv.id), 2)
                        ELSE 0 
                    END as ty_le_hoan_thanh,
                    CASE 
                        WHEN COUNT(CASE WHEN cvt.stage_type = 'done' THEN 1 END) > 0 THEN
                            ROUND(COUNT(CASE WHEN cvt.stage_type = 'done' AND cv.tre_han = false THEN 1 END) * 100.0 / 
                                  COUNT(CASE WHEN cvt.stage_type = 'done' THEN 1 END), 2)
                        ELSE 0
                    END as ty_le_dung_han,
                    COALESCE(AVG(cv.tien_do), 0) as tien_do_trung_binh,
                    COALESCE(SUM(cv.thoi_gian_uoc_tinh), 0) as thoi_gian_uoc_tinh_tong,
                    COALESCE(SUM(cv.thoi_gian_thuc_te), 0) as thoi_gian_thuc_te_tong
                FROM nhan_vien nv
                LEFT JOIN cong_viec cv ON cv.nguoi_phu_trach_id = nv.id AND cv.active = true
                LEFT JOIN cong_viec_trang_thai cvt ON cv.trang_thai_id = cvt.id
                WHERE nv.active = true
                GROUP BY nv.id, nv.phong_ban_id
            )
        """)


class HieuSuatDuAn(models.Model):
    _name = 'hieu_suat.du_an'
    _description = 'Báo cáo hiệu suất dự án'
    _auto = False
    _rec_name = 'du_an_id'
    _order = 'tien_do desc'

    du_an_id = fields.Many2one('du_an', string='Dự án', readonly=True)
    quan_ly_du_an_id = fields.Many2one('nhan_vien', string='Quản lý', readonly=True)
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', readonly=True)
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy_bo', 'Hủy bỏ')
    ], string='Trạng thái', readonly=True)
    
    tong_cong_viec = fields.Integer(string='Tổng công việc', readonly=True)
    cong_viec_hoan_thanh = fields.Integer(string='Hoàn thành', readonly=True)
    cong_viec_dang_lam = fields.Integer(string='Đang làm', readonly=True)
    cong_viec_tre_han = fields.Integer(string='Trễ hạn', readonly=True)
    
    tien_do = fields.Float(string='Tiến độ (%)', readonly=True)
    so_thanh_vien = fields.Integer(string='Số thành viên', readonly=True)

    def init(self):
        """Tạo SQL view cho báo cáo hiệu suất dự án"""
        self.env.cr.execute("""
            DROP VIEW IF EXISTS hieu_suat_du_an;
            CREATE OR REPLACE VIEW hieu_suat_du_an AS (
                SELECT
                    da.id as id,
                    da.id as du_an_id,
                    da.quan_ly_du_an_id as quan_ly_du_an_id,
                    da.phong_ban_id as phong_ban_id,
                    da.trang_thai as trang_thai,
                    COUNT(cv.id) as tong_cong_viec,
                    COUNT(CASE WHEN cvt.stage_type = 'done' THEN 1 END) as cong_viec_hoan_thanh,
                    COUNT(CASE WHEN cvt.stage_type = 'in_progress' THEN 1 END) as cong_viec_dang_lam,
                    COUNT(CASE WHEN cv.tre_han = true THEN 1 END) as cong_viec_tre_han,
                    COALESCE(AVG(cv.tien_do), 0) as tien_do,
                    da.so_thanh_vien as so_thanh_vien
                FROM du_an da
                LEFT JOIN cong_viec cv ON cv.du_an_id = da.id AND cv.active = true
                LEFT JOIN cong_viec_trang_thai cvt ON cv.trang_thai_id = cvt.id
                WHERE da.active = true
                GROUP BY da.id
            )
        """)
