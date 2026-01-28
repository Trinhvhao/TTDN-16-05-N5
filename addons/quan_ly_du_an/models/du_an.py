# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class DuAn(models.Model):
    _name = 'du_an'
    _description = 'Quản lý dự án'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ten_du_an'
    _order = 'ngay_bat_dau desc'

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_du_an = fields.Char(
        string='Mã dự án',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('du_an.sequence') or 'DA000'
    )
    ten_du_an = fields.Char(string='Tên dự án', required=True, tracking=True)
    mo_ta = fields.Html(string='Mô tả dự án')
    mo_ta_ngan = fields.Char(string='Mô tả ngắn', size=200)
    
    loai_du_an = fields.Selection([
        ('noi_bo', 'Nội bộ'),
        ('khach_hang', 'Khách hàng'),
        ('nghien_cuu', 'Nghiên cứu'),
        ('phat_trien', 'Phát triển sản phẩm'),
        ('bao_tri', 'Bảo trì'),
        ('khac', 'Khác')
    ], string='Loại dự án', default='noi_bo', tracking=True)
    
    # ==================== THỜI GIAN ====================
    ngay_bat_dau = fields.Date(string='Ngày bắt đầu', required=True, tracking=True)
    ngay_ket_thuc = fields.Date(string='Ngày kết thúc', tracking=True)
    ngay_ket_thuc_du_kien = fields.Date(string='Ngày kết thúc dự kiến')
    
    so_ngay = fields.Integer(
        string='Số ngày',
        compute='_compute_so_ngay',
        store=True
    )
    
    so_ngay_con_lai = fields.Integer(
        string='Số ngày còn lại',
        compute='_compute_so_ngay_con_lai'
    )
    
    tre_tien_do = fields.Boolean(
        string='Trễ tiến độ',
        compute='_compute_tre_tien_do',
        store=True
    )
    
    # ==================== NHÂN SỰ ====================
    quan_ly_du_an_id = fields.Many2one(
        'nhan_vien',
        string='Quản lý dự án',
        tracking=True,
        help='Người chịu trách nhiệm chính của dự án'
    )
    
    pho_quan_ly_id = fields.Many2one(
        'nhan_vien',
        string='Phó quản lý'
    )
    
    phong_ban_id = fields.Many2one(
        'phong_ban',
        string='Phòng ban phụ trách',
        tracking=True
    )
    
    thanh_vien_ids = fields.Many2many(
        'nhan_vien',
        'du_an_nhan_vien_rel',
        'du_an_id',
        'nhan_vien_id',
        string='Thành viên tham gia'
    )
    
    so_thanh_vien = fields.Integer(
        string='Số thành viên',
        compute='_compute_so_thanh_vien',
        store=True
    )
    
    # ==================== KHÁCH HÀNG ====================
    khach_hang_id = fields.Many2one(
        'res.partner',
        string='Khách hàng',
        domain=[('is_company', '=', True)]
    )
    
    lien_he_khach_hang = fields.Char(string='Người liên hệ')
    email_khach_hang = fields.Char(string='Email KH')
    dien_thoai_khach_hang = fields.Char(string='SĐT KH')
    
    # ==================== TRẠNG THÁI & TIẾN ĐỘ ====================
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('len_ke_hoach', 'Lên kế hoạch'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy_bo', 'Hủy bỏ')
    ], string='Trạng thái', default='moi', tracking=True)
    
    do_uu_tien = fields.Selection([
        ('1_thap', 'Thấp'),
        ('2_trung_binh', 'Trung bình'),
        ('3_cao', 'Cao'),
        ('4_khan_cap', 'Khẩn cấp')
    ], string='Độ ưu tiên', default='2_trung_binh', tracking=True)
    
    tien_do = fields.Float(
        string='Tiến độ (%)',
        default=0.0,
        help='Tiến độ hoàn thành dự án dựa trên các công việc'
    )
    
    muc_do_rui_ro = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao'),
        ('rat_cao', 'Rất cao')
    ], string='Mức độ rủi ro', default='thap')
    
    # ==================== NGÂN SÁCH ====================
    ngan_sach_du_kien = fields.Float(string='Ngân sách dự kiến')
    ngan_sach_thuc_te = fields.Float(string='Ngân sách thực tế', default=0.0)
    ty_le_ngan_sach = fields.Float(
        string='Tỉ lệ ngân sách (%)',
        compute='_compute_ty_le_ngan_sach'
    )
    
    doanh_thu_du_kien = fields.Float(string='Doanh thu dự kiến')
    doanh_thu_thuc_te = fields.Float(string='Doanh thu thực tế')
    loi_nhuan = fields.Float(
        string='Lợi nhuận',
        compute='_compute_loi_nhuan'
    )
    
    # ==================== TÀI LIỆU & GHI CHÚ ====================
    tai_lieu_ids = fields.One2many(
        'du_an.tai_lieu',
        'du_an_id',
        string='Tài liệu dự án'
    )
    
    moc_thoi_gian_ids = fields.One2many(
        'du_an.moc',
        'du_an_id',
        string='Mốc thời gian'
    )
    
    # ==================== CẬP NHẬT TIẾN ĐỘ ====================
    cap_nhat_ids = fields.One2many(
        'du_an.cap_nhat',
        'du_an_id',
        string='Lịch sử cập nhật'
    )
    
    last_update_id = fields.Many2one(
        'du_an.cap_nhat',
        string='Cập nhật gần nhất',
        copy=False
    )
    
    last_update_status = fields.Selection([
        ('on_track', 'Đúng tiến độ'),
        ('at_risk', 'Có rủi ro'),
        ('off_track', 'Chậm tiến độ'),
        ('on_hold', 'Tạm dừng')
    ], string='Tình trạng hiện tại', copy=False)
    
    # ==================== MILESTONE SUMMARY ====================
    milestone_count = fields.Integer(
        string='Số mốc thời gian',
        compute='_compute_milestone_stats',
        store=True
    )
    
    milestone_reached_count = fields.Integer(
        string='Số mốc đã đạt',
        compute='_compute_milestone_stats',
        store=True
    )
    
    milestone_completion_rate = fields.Float(
        string='Tỷ lệ hoàn thành mốc (%)',
        compute='_compute_milestone_stats',
        store=True
    )
    
    rui_ro_ids = fields.One2many(
        'du_an.rui_ro',
        'du_an_id',
        string='Rủi ro'
    )
    
    # ==================== KHÁC ====================
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(default=True, string='Hoạt động')
    ghi_chu = fields.Text(string='Ghi chú')
    
    tag_ids = fields.Many2many(
        'du_an.tag',
        string='Tags'
    )

    # ==================== COMPUTED FIELDS ====================
    @api.depends('thanh_vien_ids')
    def _compute_so_thanh_vien(self):
        for record in self:
            record.so_thanh_vien = len(record.thanh_vien_ids)

    @api.depends('ngay_bat_dau', 'ngay_ket_thuc_du_kien')
    def _compute_so_ngay(self):
        for record in self:
            if record.ngay_bat_dau and record.ngay_ket_thuc_du_kien:
                record.so_ngay = (record.ngay_ket_thuc_du_kien - record.ngay_bat_dau).days
            else:
                record.so_ngay = 0

    @api.depends('ngay_ket_thuc_du_kien', 'trang_thai')
    def _compute_so_ngay_con_lai(self):
        for record in self:
            if record.ngay_ket_thuc_du_kien and record.trang_thai not in ['hoan_thanh', 'huy_bo']:
                record.so_ngay_con_lai = (record.ngay_ket_thuc_du_kien - date.today()).days
            else:
                record.so_ngay_con_lai = 0

    @api.depends('ngay_ket_thuc_du_kien', 'trang_thai')
    def _compute_tre_tien_do(self):
        for record in self:
            if record.ngay_ket_thuc_du_kien and record.trang_thai not in ['hoan_thanh', 'huy_bo']:
                record.tre_tien_do = record.ngay_ket_thuc_du_kien < date.today()
            else:
                record.tre_tien_do = False

    @api.depends('ngan_sach_du_kien', 'ngan_sach_thuc_te')
    def _compute_ty_le_ngan_sach(self):
        for record in self:
            if record.ngan_sach_du_kien:
                record.ty_le_ngan_sach = (record.ngan_sach_thuc_te / record.ngan_sach_du_kien) * 100
            else:
                record.ty_le_ngan_sach = 0

    @api.depends('doanh_thu_thuc_te', 'ngan_sach_thuc_te')
    def _compute_loi_nhuan(self):
        for record in self:
            record.loi_nhuan = record.doanh_thu_thuc_te - record.ngan_sach_thuc_te

    @api.depends('moc_thoi_gian_ids', 'moc_thoi_gian_ids.is_reached')
    def _compute_milestone_stats(self):
        """Tính toán thống kê milestones"""
        for record in self:
            milestones = record.moc_thoi_gian_ids
            record.milestone_count = len(milestones)
            record.milestone_reached_count = len(milestones.filtered('is_reached'))
            
            if record.milestone_count > 0:
                record.milestone_completion_rate = (record.milestone_reached_count / record.milestone_count) * 100
            else:
                record.milestone_completion_rate = 0.0

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.ma_du_an}] {record.ten_du_an}" if record.ma_du_an else record.ten_du_an
            result.append((record.id, name))
        return result

    # ==================== ACTIONS ====================
    def action_len_ke_hoach(self):
        self.write({'trang_thai': 'len_ke_hoach'})

    def action_bat_dau(self):
        self.write({'trang_thai': 'dang_thuc_hien'})

    def action_tam_dung(self):
        self.write({'trang_thai': 'tam_dung'})

    def action_hoan_thanh(self):
        self.write({
            'trang_thai': 'hoan_thanh',
            'ngay_ket_thuc': date.today(),
            'tien_do': 100.0
        })

    def action_huy_bo(self):
        self.write({'trang_thai': 'huy_bo'})

    def action_mo_lai(self):
        self.write({'trang_thai': 'dang_thuc_hien'})

    def action_view_tai_lieu(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Tài liệu - {self.ten_du_an}',
            'res_model': 'du_an.tai_lieu',
            'view_mode': 'tree,form',
            'domain': [('du_an_id', '=', self.id)],
            'context': {'default_du_an_id': self.id}
        }
    def action_view_milestones(self):
        """Xem danh sách milestones"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Mốc thời gian - {self.ten_du_an}',
            'res_model': 'du_an.moc',
            'view_mode': 'tree,form,calendar',
            'domain': [('du_an_id', '=', self.id)],
            'context': {'default_du_an_id': self.id}
        }

    def action_view_updates(self):
        """Xem lịch sử cập nhật"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Cập nhật tiến độ - {self.ten_du_an}',
            'res_model': 'du_an.cap_nhat',
            'view_mode': 'tree,form',
            'domain': [('du_an_id', '=', self.id)],
            'context': {'default_du_an_id': self.id},
            'target': 'current'
        }

    def action_create_update(self):
        """Tạo báo cáo cập nhật mới"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo báo cáo cập nhật',
            'res_model': 'du_an.cap_nhat',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_du_an_id': self.id,
                'default_progress': self.tien_do,
                'default_status': self.last_update_status or 'on_track',
            }
        }

    def action_phan_tich_rui_ro_ai(self):
        """Sử dụng AI để phân tích rủi ro dự án"""
        self.ensure_one()
        
        try:
            # Check if ai_assistant module is installed
            if 'ai.config' not in self.env:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Module AI chưa được cài đặt',
                        'message': 'Vui lòng cài đặt module "AI Assistant" để sử dụng tính năng này.',
                        'type': 'warning',
                        'sticky': True,
                    }
                }
            
            ai_config = self.env['ai.config'].get_default_config()
            
            # Calculate milestone stats
            milestone_reached = sum(1 for m in self.milestone_ids if m.is_reached)
            
            # Chuẩn bị dữ liệu cho AI
            milestones_info = ""
            if self.milestone_ids:
                milestones_info = "\nCác mốc thời gian:\n"
                for milestone in self.milestone_ids:
                    status = "✓ Đã đạt" if milestone.is_reached else f"⏳ Còn {milestone.days_remaining} ngày"
                    milestones_info += f"- {milestone.ten_moc}: {status}\n"
            
            prompt = f"""Phân tích rủi ro chi tiết cho dự án sau:

Thông tin dự án:
- Tên: {self.ten_du_an}
- Loại: {dict(self._fields['loai_du_an'].selection).get(self.loai_du_an, 'Không xác định')}
- Trạng thái: {dict(self._fields['trang_thai'].selection).get(self.trang_thai, 'Không xác định')}
- Tiến độ: {self.tien_do}%
- Deadline: {self.ngay_ket_thuc_du_kien}
- Số ngày còn lại: {self.so_ngay_con_lai}
- Quá hạn: {'Có' if self.tre_tien_do else 'Không'}

Nhân sự:
- Quản lý dự án: {self.quan_ly_du_an_id.ho_ten if self.quan_ly_du_an_id else 'Chưa có'}
- Số thành viên: {self.so_thanh_vien}

Ngân sách:
- Dự kiến: {self.ngan_sach_du_kien:,.0f} VND
- Thực tế: {self.ngan_sach_thuc_te:,.0f} VND
- Tỷ lệ sử dụng: {self.ty_le_ngan_sach:.1f}%

Milestones:
- Tổng số: {self.milestone_count}
- Đã hoàn thành: {milestone_reached}
- Tỷ lệ: {self.milestone_completion_rate:.1f}%
{milestones_info}

Hãy phân tích và đưa ra:
1. Đánh giá tổng quan về tình trạng dự án
2. Mức độ rủi ro (Thấp/Trung bình/Cao/Rất cao) và lý do
3. Các rủi ro tiềm ẩn chính (ít nhất 3-5 rủi ro)
4. Giải pháp đề xuất cụ thể cho từng rủi ro
5. Khuyến nghị hành động ngay (nếu có)

Trả lời bằng tiếng Việt, chi tiết và có cấu trúc rõ ràng."""

            result = ai_config.call_ai(prompt, context_type='risk_analysis')
            
            if result.get('error'):
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Lỗi khi gọi AI',
                        'message': result.get('error'),
                        'type': 'danger',
                        'sticky': True,
                    }
                }
            
            # Hiển thị kết quả
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': f'📊 Phân tích Rủi ro AI - {self.ten_du_an}',
                    'message': result.get('response', 'Không có kết quả'),
                    'type': 'info',
                    'sticky': True,
                }
            }
            
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Lỗi',
                    'message': f'Không thể phân tích rủi ro: {str(e)}',
                    'type': 'warning',
                    'sticky': False,
                }
            }
    def action_view_rui_ro(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Rủi ro - {self.ten_du_an}',
            'res_model': 'du_an.rui_ro',
            'view_mode': 'tree,form',
            'domain': [('du_an_id', '=', self.id)],
            'context': {'default_du_an_id': self.id}
        }

    _sql_constraints = [
        ('ma_du_an_unique', 'UNIQUE(ma_du_an)', 'Mã dự án phải là duy nhất!')
    ]


class DuAnTag(models.Model):
    _name = 'du_an.tag'
    _description = 'Tag dự án'

    name = fields.Char(string='Tên tag', required=True)
    color = fields.Integer(string='Color')


class DuAnTaiLieu(models.Model):
    _name = 'du_an.tai_lieu'
    _description = 'Tài liệu dự án'
    _order = 'ngay_tao desc'

    du_an_id = fields.Many2one('du_an', string='Dự án', required=True, ondelete='cascade')
    ten_tai_lieu = fields.Char(string='Tên tài liệu', required=True)
    loai_tai_lieu = fields.Selection([
        ('hop_dong', 'Hợp đồng'),
        ('bao_cao', 'Báo cáo'),
        ('thiet_ke', 'Thiết kế'),
        ('huong_dan', 'Hướng dẫn'),
        ('bien_ban', 'Biên bản'),
        ('khac', 'Khác')
    ], string='Loại tài liệu', default='khac')
    
    file = fields.Binary(string='File', required=True)
    file_name = fields.Char(string='Tên file')
    mo_ta = fields.Text(string='Mô tả')
    
    nguoi_tao_id = fields.Many2one('nhan_vien', string='Người tạo')
    ngay_tao = fields.Date(string='Ngày tạo', default=fields.Date.today)
    
    phien_ban = fields.Char(string='Phiên bản', default='1.0')


class DuAnMoc(models.Model):
    _name = 'du_an.moc'
    _description = 'Mốc thời gian dự án'
    _order = 'ngay_muc_tieu'

    du_an_id = fields.Many2one('du_an', string='Dự án', required=True, ondelete='cascade')
    ten_moc = fields.Char(string='Tên mốc', required=True)
    mo_ta = fields.Text(string='Mô tả')
    
    ngay_muc_tieu = fields.Date(string='Ngày mục tiêu', required=True)
    ngay_hoan_thanh = fields.Date(string='Ngày hoàn thành')
    
    trang_thai = fields.Selection([
        ('chua_dat', 'Chưa đạt'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('da_dat', 'Đã đạt'),
        ('tre_han', 'Trễ hạn')
    ], string='Trạng thái', default='chua_dat')
    
    nguoi_phu_trach_id = fields.Many2one('nhan_vien', string='Người phụ trách')

    @api.onchange('ngay_hoan_thanh')
    def _onchange_ngay_hoan_thanh(self):
        if self.ngay_hoan_thanh:
            self.trang_thai = 'da_dat'


class DuAnRuiRo(models.Model):
    _name = 'du_an.rui_ro'
    _description = 'Rủi ro dự án'

    du_an_id = fields.Many2one('du_an', string='Dự án', required=True, ondelete='cascade')
    ten_rui_ro = fields.Char(string='Tên rủi ro', required=True)
    mo_ta = fields.Text(string='Mô tả')
    
    xac_suat = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao')
    ], string='Xác suất xảy ra', default='thap')
    
    muc_do_anh_huong = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao'),
        ('nghiem_trong', 'Nghiêm trọng')
    ], string='Mức độ ảnh hưởng', default='trung_binh')
    
    bien_phap_phong_ngua = fields.Text(string='Biện pháp phòng ngừa')
    bien_phap_xu_ly = fields.Text(string='Biện pháp xử lý')
    
    trang_thai = fields.Selection([
        ('tiem_an', 'Tiềm ẩn'),
        ('dang_xy_ly', 'Đang xử lý'),
        ('da_xu_ly', 'Đã xử lý'),
        ('da_xay_ra', 'Đã xảy ra')
    ], string='Trạng thái', default='tiem_an')
    
    nguoi_phu_trach_id = fields.Many2one('nhan_vien', string='Người phụ trách')
