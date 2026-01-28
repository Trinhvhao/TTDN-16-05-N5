# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Thông tin nhân viên'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ho_ten'

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_nhan_vien = fields.Char(
        string='Mã nhân viên',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('nhan_vien.sequence') or 'NV000'
    )
    ho_ten_dem = fields.Char(string='Họ và tên đệm')
    ten = fields.Char(string='Tên', required=True)
    ho_ten = fields.Char(
        string='Họ và tên',
        compute='_compute_ho_ten',
        store=True
    )
    
    # ==================== THÔNG TIN CÁ NHÂN ====================
    ngay_sinh = fields.Date(string='Ngày sinh')
    tuoi = fields.Integer(string='Tuổi', compute='_compute_tuoi', store=True)
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác')
    ], string='Giới tính', default='nam')
    
    cmnd_cccd = fields.Char(string='CMND/CCCD')
    ngay_cap_cmnd = fields.Date(string='Ngày cấp')
    noi_cap_cmnd = fields.Char(string='Nơi cấp')
    
    quoc_tich = fields.Many2one('res.country', string='Quốc tịch', default=lambda self: self.env.ref('base.vn', raise_if_not_found=False))
    dan_toc = fields.Char(string='Dân tộc', default='Kinh')
    ton_giao = fields.Char(string='Tôn giáo')
    
    tinh_trang_hon_nhan = fields.Selection([
        ('doc_than', 'Độc thân'),
        ('da_ket_hon', 'Đã kết hôn'),
        ('ly_hon', 'Ly hôn'),
        ('goa', 'Góa')
    ], string='Tình trạng hôn nhân', default='doc_than')
    
    # ==================== ĐỊA CHỈ ====================
    dia_chi = fields.Text(string='Địa chỉ hiện tại')
    que_quan = fields.Char(string='Quê quán')
    dia_chi_thuong_tru = fields.Text(string='Địa chỉ thường trú')
    
    # Địa chỉ chi tiết
    tinh_thanh_id = fields.Many2one('res.country.state', string='Tỉnh/Thành phố', domain="[('country_id.code', '=', 'VN')]")
    quan_huyen = fields.Char(string='Quận/Huyện')
    phuong_xa = fields.Char(string='Phường/Xã')
    
    # ==================== THÔNG TIN LIÊN LẠC ====================
    email = fields.Char(string='Email cá nhân')
    email_cong_ty = fields.Char(string='Email công ty')
    dien_thoai = fields.Char(string='Số điện thoại')
    dien_thoai_khan_cap = fields.Char(string='SĐT khẩn cấp')
    nguoi_lien_he_khan_cap = fields.Char(string='Người liên hệ khẩn cấp')
    quan_he_khan_cap = fields.Char(string='Quan hệ với người LH khẩn cấp')
    
    # ==================== THÔNG TIN CÔNG VIỆC ====================
    phong_ban_id = fields.Many2one(
        'phong_ban',
        string='Phòng ban',
        tracking=True
    )
    chuc_vu_id = fields.Many2one(
        'chuc_vu',
        string='Chức vụ',
        tracking=True
    )
    
    cap_bac = fields.Selection([
        ('nhan_vien', 'Nhân viên'),
        ('truong_nhom', 'Trưởng nhóm'),
        ('pho_phong', 'Phó phòng'),
        ('truong_phong', 'Trưởng phòng'),
        ('pho_giam_doc', 'Phó giám đốc'),
        ('giam_doc', 'Giám đốc'),
        ('chu_tich', 'Chủ tịch')
    ], string='Cấp bậc', default='nhan_vien')
    
    ngay_vao_lam = fields.Date(string='Ngày vào làm', tracking=True)
    ngay_chinh_thuc = fields.Date(string='Ngày chính thức')
    ngay_nghi_viec = fields.Date(string='Ngày nghỉ việc')
    
    tham_nien = fields.Float(
        string='Thâm niên (năm)',
        compute='_compute_tham_nien',
        store=True
    )
    
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('co_thoi_han', 'Có thời hạn'),
        ('khong_thoi_han', 'Không thời hạn'),
        ('thoi_vu', 'Thời vụ'),
        ('cong_tac_vien', 'Cộng tác viên')
    ], string='Loại hợp đồng', default='thu_viec', tracking=True)
    
    trang_thai = fields.Selection([
        ('dang_lam', 'Đang làm việc'),
        ('nghi_phep', 'Nghỉ phép'),
        ('nghi_thai_san', 'Nghỉ thai sản'),
        ('nghi_om', 'Nghỉ ốm'),
        ('nghi_khong_luong', 'Nghỉ không lương'),
        ('tam_nghi', 'Tạm nghỉ'),
        ('nghi_viec', 'Nghỉ việc'),
        ('thu_viec', 'Thử việc')
    ], string='Trạng thái', default='thu_viec', tracking=True)
    
    ly_do_nghi_viec = fields.Text(string='Lý do nghỉ việc')
    
    # ==================== LƯƠNG & PHỤ CẤP ====================
    luong_co_ban = fields.Float(string='Lương cơ bản', tracking=True)
    phu_cap_an_trua = fields.Float(string='Phụ cấp ăn trưa')
    phu_cap_di_lai = fields.Float(string='Phụ cấp đi lại')
    phu_cap_dien_thoai = fields.Float(string='Phụ cấp điện thoại')
    phu_cap_khac = fields.Float(string='Phụ cấp khác')
    
    tong_thu_nhap = fields.Float(
        string='Tổng thu nhập',
        compute='_compute_tong_thu_nhap',
        store=True
    )
    
    so_tai_khoan = fields.Char(string='Số tài khoản')
    ngan_hang = fields.Char(string='Ngân hàng')
    chi_nhanh_nh = fields.Char(string='Chi nhánh NH')
    
    ma_so_thue = fields.Char(string='Mã số thuế cá nhân')
    so_bhxh = fields.Char(string='Số BHXH')
    so_bhyt = fields.Char(string='Số BHYT')
    
    # ==================== HỌC VẤN & KỸ NĂNG ====================
    trinh_do_hoc_van = fields.Selection([
        ('thpt', 'THPT'),
        ('trung_cap', 'Trung cấp'),
        ('cao_dang', 'Cao đẳng'),
        ('dai_hoc', 'Đại học'),
        ('thac_si', 'Thạc sĩ'),
        ('tien_si', 'Tiến sĩ')
    ], string='Trình độ học vấn')
    
    chuyen_nganh = fields.Char(string='Chuyên ngành')
    truong_tot_nghiep = fields.Char(string='Trường tốt nghiệp')
    nam_tot_nghiep = fields.Integer(string='Năm tốt nghiệp')
    
    ky_nang_ids = fields.Many2many('nhan_vien.ky_nang', string='Kỹ năng')
    chung_chi_ids = fields.One2many('nhan_vien.chung_chi', 'nhan_vien_id', string='Chứng chỉ')
    
    ngoai_ngu = fields.Char(string='Ngoại ngữ')
    trinh_do_ngoai_ngu = fields.Selection([
        ('co_ban', 'Cơ bản'),
        ('trung_binh', 'Trung bình'),
        ('kha', 'Khá'),
        ('tot', 'Tốt'),
        ('gioi', 'Giỏi'),
        ('ban_ngu', 'Bản ngữ')
    ], string='Trình độ ngoại ngữ')
    
    # ==================== QUAN HỆ ====================
    lich_su_lam_viec_ids = fields.One2many(
        'lich_su_lam_viec',
        'nhan_vien_id',
        string='Lịch sử làm việc'
    )
    
    nguoi_phu_thuoc_ids = fields.One2many(
        'nhan_vien.nguoi_phu_thuoc',
        'nhan_vien_id',
        string='Người phụ thuộc'
    )
    
    hop_dong_ids = fields.One2many(
        'nhan_vien.hop_dong',
        'nhan_vien_id',
        string='Hợp đồng lao động'
    )
    
    # Liên kết với user hệ thống
    user_id = fields.Many2one(
        'res.users',
        string='Tài khoản người dùng',
        help='Tài khoản đăng nhập hệ thống của nhân viên.'
    )
    
    manager_id = fields.Many2one(
        'nhan_vien',
        string='Quản lý trực tiếp'
    )
    
    subordinate_ids = fields.One2many(
        'nhan_vien',
        'manager_id',
        string='Nhân viên cấp dưới'
    )
    
    so_nhan_vien_cap_duoi = fields.Integer(
        string='Số NV cấp dưới',
        compute='_compute_so_nhan_vien_cap_duoi'
    )
    
    # ==================== ẢNH & TÀI LIỆU ====================
    anh_dai_dien = fields.Binary(string='Ảnh đại diện')
    
    # ==================== KHÁC ====================
    active = fields.Boolean(default=True, string='Hoạt động')
    ghi_chu = fields.Text(string='Ghi chú')
    
    color = fields.Integer(string='Color Index')
    
    # ==================== COMPUTED FIELDS ====================
    @api.depends('ho_ten_dem', 'ten')
    def _compute_ho_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_ten = f"{record.ho_ten_dem} {record.ten}"
            elif record.ten:
                record.ho_ten = record.ten
            else:
                record.ho_ten = ''

    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                today = date.today()
                record.tuoi = today.year - record.ngay_sinh.year - (
                    (today.month, today.day) < (record.ngay_sinh.month, record.ngay_sinh.day)
                )
            else:
                record.tuoi = 0

    @api.depends('ngay_vao_lam')
    def _compute_tham_nien(self):
        for record in self:
            if record.ngay_vao_lam:
                today = date.today()
                delta = relativedelta(today, record.ngay_vao_lam)
                record.tham_nien = delta.years + delta.months / 12
            else:
                record.tham_nien = 0.0

    @api.depends('luong_co_ban', 'phu_cap_an_trua', 'phu_cap_di_lai', 'phu_cap_dien_thoai', 'phu_cap_khac')
    def _compute_tong_thu_nhap(self):
        for record in self:
            record.tong_thu_nhap = (
                record.luong_co_ban +
                record.phu_cap_an_trua +
                record.phu_cap_di_lai +
                record.phu_cap_dien_thoai +
                record.phu_cap_khac
            )

    @api.depends('subordinate_ids')
    def _compute_so_nhan_vien_cap_duoi(self):
        for record in self:
            record.so_nhan_vien_cap_duoi = len(record.subordinate_ids)

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.ma_nhan_vien}] {record.ho_ten}" if record.ho_ten else record.ma_nhan_vien
            result.append((record.id, name))
        return result

    # ==================== ACTIONS ====================
    def action_set_dang_lam(self):
        self.write({'trang_thai': 'dang_lam'})
    
    def action_set_nghi_phep(self):
        self.write({'trang_thai': 'nghi_phep'})
    
    def action_set_nghi_viec(self):
        self.write({
            'trang_thai': 'nghi_viec',
            'ngay_nghi_viec': date.today()
        })

    def action_view_hop_dong(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Hợp đồng - {self.ho_ten}',
            'res_model': 'nhan_vien.hop_dong',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_id', '=', self.id)],
            'context': {'default_nhan_vien_id': self.id}
        }

    def action_view_subordinates(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Nhân viên cấp dưới - {self.ho_ten}',
            'res_model': 'nhan_vien',
            'view_mode': 'tree,kanban,form',
            'domain': [('manager_id', '=', self.id)]
        }

    _sql_constraints = [
        ('ma_nhan_vien_unique', 'UNIQUE(ma_nhan_vien)', 'Mã nhân viên phải là duy nhất!'),
        ('cmnd_cccd_unique', 'UNIQUE(cmnd_cccd)', 'CMND/CCCD phải là duy nhất!')
    ]


class NhanVienKyNang(models.Model):
    _name = 'nhan_vien.ky_nang'
    _description = 'Kỹ năng nhân viên'

    name = fields.Char(string='Tên kỹ năng', required=True)
    loai_ky_nang = fields.Selection([
        ('ky_thuat', 'Kỹ thuật'),
        ('mem', 'Mềm'),
        ('quan_ly', 'Quản lý'),
        ('ngoai_ngu', 'Ngoại ngữ'),
        ('khac', 'Khác')
    ], string='Loại kỹ năng', default='ky_thuat')
    mo_ta = fields.Text(string='Mô tả')
    color = fields.Integer(string='Color')


class NhanVienChungChi(models.Model):
    _name = 'nhan_vien.chung_chi'
    _description = 'Chứng chỉ nhân viên'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='cascade')
    ten_chung_chi = fields.Char(string='Tên chứng chỉ', required=True)
    to_chuc_cap = fields.Char(string='Tổ chức cấp')
    ngay_cap = fields.Date(string='Ngày cấp')
    ngay_het_han = fields.Date(string='Ngày hết hạn')
    file_dinh_kem = fields.Binary(string='File đính kèm')
    ghi_chu = fields.Text(string='Ghi chú')
    
    con_hieu_luc = fields.Boolean(
        string='Còn hiệu lực',
        compute='_compute_con_hieu_luc'
    )

    @api.depends('ngay_het_han')
    def _compute_con_hieu_luc(self):
        for record in self:
            if record.ngay_het_han:
                record.con_hieu_luc = record.ngay_het_han >= date.today()
            else:
                record.con_hieu_luc = True


class NhanVienNguoiPhuThuoc(models.Model):
    _name = 'nhan_vien.nguoi_phu_thuoc'
    _description = 'Người phụ thuộc của nhân viên'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='cascade')
    ho_ten = fields.Char(string='Họ tên', required=True)
    quan_he = fields.Selection([
        ('vo_chong', 'Vợ/Chồng'),
        ('con', 'Con'),
        ('cha_me', 'Cha/Mẹ'),
        ('anh_chi_em', 'Anh/Chị/Em'),
        ('khac', 'Khác')
    ], string='Quan hệ', required=True)
    ngay_sinh = fields.Date(string='Ngày sinh')
    cmnd_cccd = fields.Char(string='CMND/CCCD')
    ngay_dang_ky = fields.Date(string='Ngày đăng ký phụ thuộc')
    ngay_het_hieu_luc = fields.Date(string='Ngày hết hiệu lực')
    ghi_chu = fields.Text(string='Ghi chú')


class NhanVienHopDong(models.Model):
    _name = 'nhan_vien.hop_dong'
    _description = 'Hợp đồng lao động'
    _order = 'ngay_bat_dau desc'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='cascade')
    ma_hop_dong = fields.Char(
        string='Mã hợp đồng',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('nhan_vien.hop_dong') or 'HD000'
    )
    
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('co_thoi_han', 'Có thời hạn'),
        ('khong_thoi_han', 'Không thời hạn'),
        ('thoi_vu', 'Thời vụ'),
        ('phu_luc', 'Phụ lục hợp đồng')
    ], string='Loại hợp đồng', required=True)
    
    ngay_bat_dau = fields.Date(string='Ngày bắt đầu', required=True)
    ngay_ket_thuc = fields.Date(string='Ngày kết thúc')
    
    luong_co_ban = fields.Float(string='Lương cơ bản')
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('hieu_luc', 'Có hiệu lực'),
        ('het_han', 'Hết hạn'),
        ('cham_dut', 'Chấm dứt')
    ], string='Trạng thái', default='nhap')
    
    file_hop_dong = fields.Binary(string='File hợp đồng')
    ghi_chu = fields.Text(string='Ghi chú')

    def action_xac_nhan(self):
        self.write({'trang_thai': 'hieu_luc'})
        # Cập nhật loại hợp đồng và lương cho nhân viên
        self.nhan_vien_id.write({
            'loai_hop_dong': self.loai_hop_dong,
            'luong_co_ban': self.luong_co_ban
        })

    def action_cham_dut(self):
        self.write({'trang_thai': 'cham_dut'})
