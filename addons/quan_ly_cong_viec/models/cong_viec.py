# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class CongViec(models.Model):
    _name = 'cong_viec'
    _description = 'Quản lý công việc/tác vụ'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ten_cong_viec'
    _order = 'do_uu_tien desc, ngay_ket_thuc asc'

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_cong_viec = fields.Char(
        string='Mã công việc',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('cong_viec.sequence') or 'CV000'
    )
    ten_cong_viec = fields.Char(string='Tên công việc', required=True, tracking=True)
    mo_ta = fields.Html(string='Mô tả chi tiết')
    
    loai_cong_viec = fields.Selection([
        ('task', 'Task'),
        ('bug', 'Bug'),
        ('feature', 'Feature'),
        ('improvement', 'Improvement'),
        ('research', 'Nghiên cứu'),
        ('meeting', 'Họp'),
        ('other', 'Khác')
    ], string='Loại công việc', default='task', tracking=True)
    
    # ==================== LIÊN KẾT ====================
    du_an_id = fields.Many2one(
        'du_an',
        string='Dự án',
        ondelete='cascade',
        tracking=True,
        required=True
    )
    
    giai_doan = fields.Selection([
        ('phan_tich', 'Phân tích'),
        ('thiet_ke', 'Thiết kế'),
        ('phat_trien', 'Phát triển'),
        ('kiem_thu', 'Kiểm thử'),
        ('trien_khai', 'Triển khai'),
        ('bao_tri', 'Bảo trì')
    ], string='Giai đoạn', default='phat_trien')
    
    # ==================== PHÂN CÔNG ====================
    nguoi_phu_trach_id = fields.Many2one(
        'nhan_vien',
        string='Người phụ trách',
        tracking=True,
        required=True
    )
    
    nguoi_tao_id = fields.Many2one(
        'nhan_vien',
        string='Người tạo'
    )
    
    nguoi_kiem_tra_id = fields.Many2one(
        'nhan_vien',
        string='Người kiểm tra'
    )
    
    nguoi_ho_tro_ids = fields.Many2many(
        'nhan_vien',
        'cong_viec_nguoi_ho_tro_rel',
        'cong_viec_id',
        'nhan_vien_id',
        string='Người hỗ trợ'
    )
    
    # ==================== THỜI GIAN ====================
    ngay_bat_dau = fields.Date(
        string='Ngày bắt đầu',
        default=fields.Date.today,
        tracking=True
    )
    ngay_ket_thuc = fields.Date(string='Ngày kết thúc', tracking=True)
    ngay_hoan_thanh_thuc_te = fields.Date(string='Ngày hoàn thành thực tế')
    
    thoi_gian_uoc_tinh = fields.Float(string='Thời gian ước tính (giờ)')
    thoi_gian_thuc_te = fields.Float(string='Thời gian thực tế (giờ)')
    
    hieu_suat = fields.Float(
        string='Hiệu suất (%)',
        compute='_compute_hieu_suat',
        store=True
    )
    
    so_ngay_con_lai = fields.Integer(
        string='Số ngày còn lại',
        compute='_compute_so_ngay_con_lai',
        store=True
    )
    
    tre_han = fields.Boolean(
        string='Trễ hạn',
        compute='_compute_tre_han',
        store=True
    )
    
    # ==================== TRẠNG THÁI & TIẾN ĐỘ ====================
    trang_thai_id = fields.Many2one(
        'cong_viec.trang_thai',
        string='Trạng thái',
        tracking=True,
        index=True,
        group_expand='_read_group_trang_thai_ids',
        copy=False,
        domain="['|', ('du_an_ids', '=', False), ('du_an_ids', '=', du_an_id)]"
    )
    
    stage_type = fields.Selection(
        related='trang_thai_id.stage_type',
        string='Loại trạng thái',
        store=True,
        readonly=True
    )
    
    # Kanban state for task status indicator
    kanban_state = fields.Selection([
        ('normal', 'Bình thường'),
        ('done', 'Sẵn sàng'),
        ('blocked', 'Bị chặn')
    ], string='Kanban State', default='normal', required=True, tracking=True,
       help='* Bình thường: Công việc đang tiến hành bình thường\n'
            '* Sẵn sàng: Công việc sẵn sàng để chuyển sang stage tiếp theo\n'
            '* Bị chặn: Công việc bị chặn bởi vấn đề nào đó')
    
    do_uu_tien = fields.Selection([
        ('1', 'Thấp'),
        ('2', 'Trung bình'),
        ('3', 'Cao'),
        ('4', 'Khẩn cấp')
    ], string='Độ ưu tiên', default='2', tracking=True)
    
    tien_do = fields.Float(
        string='Tiến độ (%)',
        default=0.0,
        tracking=True,
        help='Phần trăm hoàn thành công việc (0-100)'
    )
    
    do_kho = fields.Selection([
        ('de', 'Dễ'),
        ('trung_binh', 'Trung bình'),
        ('kho', 'Khó'),
        ('rat_kho', 'Rất khó')
    ], string='Độ khó', default='trung_binh')
    
    # ==================== CHI PHÍ ====================
    chi_phi = fields.Float(string='Chi phí')
    
    # ==================== CÔNG VIỆC CON ====================
    parent_id = fields.Many2one(
        'cong_viec',
        string='Công việc cha',
        ondelete='cascade'
    )
    
    child_ids = fields.One2many(
        'cong_viec',
        'parent_id',
        string='Công việc con'
    )
    
    so_cong_viec_con = fields.Integer(
        string='Số công việc con',
        compute='_compute_so_cong_viec_con',
        store=True
    )
    
    # ==================== TASK DEPENDENCIES ====================
    depends_on_ids = fields.Many2many(
        'cong_viec',
        'cong_viec_dependency_rel',
        'cong_viec_id',
        'depends_on_id',
        string='Phụ thuộc vào',
        help='Công việc này phụ thuộc vào các công việc khác (phải hoàn thành trước)'
    )
    
    blocked_by_ids = fields.Many2many(
        'cong_viec',
        'cong_viec_dependency_rel',
        'depends_on_id',
        'cong_viec_id',
        string='Chặn các công việc',
        help='Công việc này chặn các công việc khác (phải hoàn thành trước)'
    )
    
    can_start = fields.Boolean(
        string='Có thể bắt đầu',
        compute='_compute_can_start',
        help='Kiểm tra xem tất cả dependencies đã hoàn thành chưa'
    )
    
    # ==================== RECURRING TASKS ====================
    is_recurring = fields.Boolean(
        string='Công việc định kỳ',
        default=False,
        help='Công việc này sẽ tự động tạo lại theo chu kỳ'
    )
    
    recurrence_type = fields.Selection([
        ('daily', 'Hàng ngày'),
        ('weekly', 'Hàng tuần'),
        ('monthly', 'Hàng tháng'),
        ('yearly', 'Hàng năm')
    ], string='Loại lặp lại', help='Chu kỳ lặp lại công việc')
    
    recurrence_interval = fields.Integer(
        string='Khoảng lặp',
        default=1,
        help='Số lượng ngày/tuần/tháng/năm giữa các lần lặp'
    )
    
    recurrence_end_date = fields.Date(
        string='Ngày kết thúc lặp',
        help='Ngày dừng tạo công việc định kỳ. Để trống nếu lặp vô hạn'
    )
    
    next_recurrence_date = fields.Date(
        string='Ngày tạo lần tiếp theo',
        help='Ngày tạo công việc định kỳ tiếp theo'
    )
    
    parent_recurring_task_id = fields.Many2one(
        'cong_viec',
        string='Công việc định kỳ gốc',
        help='Công việc định kỳ gốc tạo ra công việc này'
    )
    
    # ==================== CHECKLIST ====================
    checklist_ids = fields.One2many(
        'cong_viec.checklist',
        'cong_viec_id',
        string='Checklist'
    )
    
    tien_do_checklist = fields.Float(
        string='Tiến độ checklist',
        compute='_compute_tien_do_checklist'
    )
    
    # ==================== BÌNH LUẬN & LOG ====================
    gio_lam_viec_ids = fields.One2many(
        'cong_viec.timesheet',
        'cong_viec_id',
        string='Giờ làm việc'
    )
    
    tong_gio_log = fields.Float(
        string='Tổng giờ log',
        compute='_compute_tong_gio_log',
        store=True
    )
    
    # ==================== NHÃN & KHÁC ====================
    tag_ids = fields.Many2many(
        'cong_viec.tag',
        string='Nhãn'
    )
    
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(default=True, string='Hoạt động')
    ghi_chu = fields.Text(string='Ghi chú')
    
    # Link issue/ticket
    link_issue = fields.Char(string='Link issue/ticket')

    # ==================== COMPUTED FIELDS ====================
    @api.depends('ngay_ket_thuc', 'trang_thai_id.stage_type')
    def _compute_so_ngay_con_lai(self):
        for record in self:
            if record.ngay_ket_thuc and record.trang_thai_id.stage_type not in ['done', 'cancelled']:
                record.so_ngay_con_lai = (record.ngay_ket_thuc - date.today()).days
            else:
                record.so_ngay_con_lai = 0

    @api.depends('ngay_ket_thuc', 'trang_thai_id.stage_type')
    def _compute_tre_han(self):
        for record in self:
            if record.ngay_ket_thuc and record.trang_thai_id.stage_type not in ['done', 'cancelled']:
                record.tre_han = record.ngay_ket_thuc < date.today()
            else:
                record.tre_han = False

    @api.depends('child_ids')
    def _compute_so_cong_viec_con(self):
        for record in self:
            record.so_cong_viec_con = len(record.child_ids)
    
    @api.depends('depends_on_ids', 'depends_on_ids.trang_thai_id.stage_type')
    def _compute_can_start(self):
        """Kiểm tra xem tất cả dependencies đã hoàn thành chưa"""
        for record in self:
            if not record.depends_on_ids:
                record.can_start = True
            else:
                # Kiểm tra tất cả dependencies đã hoàn thành
                record.can_start = all(
                    dep.trang_thai_id.stage_type == 'done' 
                    for dep in record.depends_on_ids
                )

    @api.depends('thoi_gian_uoc_tinh', 'thoi_gian_thuc_te')
    def _compute_hieu_suat(self):
        for record in self:
            if record.thoi_gian_thuc_te > 0:
                record.hieu_suat = (record.thoi_gian_uoc_tinh / record.thoi_gian_thuc_te) * 100
            else:
                record.hieu_suat = 0

    @api.depends('checklist_ids', 'checklist_ids.done')
    def _compute_tien_do_checklist(self):
        for record in self:
            if record.checklist_ids:
                done = len(record.checklist_ids.filtered('done'))
                total = len(record.checklist_ids)
                record.tien_do_checklist = (done / total) * 100
            else:
                record.tien_do_checklist = 0

    @api.depends('gio_lam_viec_ids', 'gio_lam_viec_ids.so_gio')
    def _compute_tong_gio_log(self):
        for record in self:
            record.tong_gio_log = sum(record.gio_lam_viec_ids.mapped('so_gio'))

    @api.onchange('tien_do')
    def _onchange_tien_do(self):
        if self.tien_do >= 100:
            self.tien_do = 100.0
        elif self.tien_do < 0:
            self.tien_do = 0.0
    
    @api.constrains('depends_on_ids')
    def _check_dependency_recursion(self):
        """Kiểm tra không có vòng lặp trong dependencies"""
        for record in self:
            if not record._check_recursion_dependencies():
                raise models.ValidationError(
                    'Lỗi: Phát hiện vòng lặp trong các phụ thuộc công việc! '
                    'Không thể tạo phụ thuộc vòng tròn.'
                )
    
    def _check_recursion_dependencies(self, visited=None):
        """Kiểm tra đệ quy để phát hiện vòng lặp"""
        if visited is None:
            visited = set()
        
        if self.id in visited:
            return False
        
        visited.add(self.id)
        
        for dep in self.depends_on_ids:
            if not dep._check_recursion_dependencies(visited.copy()):
                return False
        
        return True
    
    @api.constrains('is_recurring', 'recurrence_type', 'recurrence_interval')
    def _check_recurring_fields(self):
        """Validate recurring task fields"""
        for record in self:
            if record.is_recurring:
                if not record.recurrence_type:
                    raise models.ValidationError('Vui lòng chọn loại lặp lại cho công việc định kỳ!')
                if record.recurrence_interval < 1:
                    raise models.ValidationError('Khoảng lặp phải lớn hơn 0!')

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.ma_cong_viec}] {record.ten_cong_viec}" if record.ma_cong_viec else record.ten_cong_viec
            result.append((record.id, name))
        return result

    # ==================== ACTIONS ====================
    def action_chua_lam(self):
        # Tìm stage "Chưa làm"
        stage_chua_lam = self.env.ref('quan_ly_cong_viec.stage_chua_lam', raise_if_not_found=False)
        if stage_chua_lam:
            self.write({'trang_thai_id': stage_chua_lam.id})

    def action_bat_dau(self):
        # Tìm stage "Đang làm"
        stage_dang_lam = self.env.ref('quan_ly_cong_viec.stage_dang_lam', raise_if_not_found=False)
        if stage_dang_lam:
            self.write({
                'trang_thai_id': stage_dang_lam.id,
                'ngay_bat_dau': fields.Date.today() if not self.ngay_bat_dau else self.ngay_bat_dau
            })

    def action_review(self):
        # Tìm stage "Review"
        stage_review = self.env.ref('quan_ly_cong_viec.stage_review', raise_if_not_found=False)
        if stage_review:
            self.write({'trang_thai_id': stage_review.id})

    def action_cho_kiem_tra(self):
        # Tìm stage "Chờ kiểm tra"
        stage_cho_kiem_tra = self.env.ref('quan_ly_cong_viec.stage_cho_kiem_tra', raise_if_not_found=False)
        if stage_cho_kiem_tra:
            self.write({'trang_thai_id': stage_cho_kiem_tra.id})

    def action_hoan_thanh(self):
        # Tìm stage "Hoàn thành"
        stage_hoan_thanh = self.env.ref('quan_ly_cong_viec.stage_hoan_thanh', raise_if_not_found=False)
        if stage_hoan_thanh:
            self.write({
                'trang_thai_id': stage_hoan_thanh.id,
                'tien_do': 100.0,
                'ngay_hoan_thanh_thuc_te': fields.Date.today()
            })

    def action_huy_bo(self):
        # Cập nhật để dùng trang_thai_id thay vì trang_thai
        stage_huy_bo = self.env.ref('quan_ly_cong_viec.stage_huy_bo', raise_if_not_found=False)
        if stage_huy_bo:
            self.write({'trang_thai_id': stage_huy_bo.id})

    def action_mo_lai(self):
        # Cập nhật để dùng trang_thai_id thay vì trang_thai
        stage_dang_lam = self.env.ref('quan_ly_cong_viec.stage_dang_lam', raise_if_not_found=False)
        if stage_dang_lam:
            self.write({
                'trang_thai_id': stage_dang_lam.id,
                'ngay_hoan_thanh_thuc_te': False
            })

    @api.model
    def _read_group_trang_thai_ids(self, stages, domain, order):
        """
        Read group customization để hiển thị tất cả các stages trong kanban view,
        ngay cả khi chúng trống
        """
        # Lấy du_an_id từ context
        du_an_id = self.env.context.get('default_du_an_id')
        
        if du_an_id:
            # Tìm stages của dự án này hoặc stages chung
            search_domain = ['|', ('du_an_ids', '=', False), ('du_an_ids', '=', du_an_id)]
        else:
            # Hiển thị tất cả stages
            search_domain = []
        
        # Thực hiện search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=1)
        return stages.browse(stage_ids)

    def action_view_subtasks(self):
        """Mở danh sách công việc con"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Công việc con - {self.ten_cong_viec}',
            'res_model': 'cong_viec',
            'view_mode': 'tree,kanban,form',
            'domain': [('parent_id', '=', self.id)],
            'context': {
                'default_parent_id': self.id,
                'default_du_an_id': self.du_an_id.id,
            }
        }

    def action_log_time(self):
        """Mở form log giờ làm việc"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Log giờ làm việc',
            'res_model': 'cong_viec.timesheet',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_cong_viec_id': self.id,
                'default_nhan_vien_id': self.nguoi_phu_trach_id.id,
            }
        }
    
    # ==================== RECURRING TASKS METHODS ====================
    def _calculate_next_recurrence_date(self):
        """Tính toán ngày tạo recurring task tiếp theo"""
        self.ensure_one()
        
        if not self.is_recurring or not self.recurrence_type:
            return False
        
        base_date = self.next_recurrence_date or self.ngay_ket_thuc or fields.Date.today()
        interval = self.recurrence_interval or 1
        
        if self.recurrence_type == 'daily':
            return base_date + timedelta(days=interval)
        elif self.recurrence_type == 'weekly':
            return base_date + timedelta(weeks=interval)
        elif self.recurrence_type == 'monthly':
            # Thêm số tháng (xử lý tháng cuối năm)
            month = base_date.month + interval
            year = base_date.year + (month - 1) // 12
            month = ((month - 1) % 12) + 1
            day = min(base_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
            return date(year, month, day)
        elif self.recurrence_type == 'yearly':
            year = base_date.year + interval
            month = base_date.month
            day = min(base_date.day, 29 if month == 2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else base_date.day)
            return date(year, month, day)
        
        return False
    
    def _create_recurring_task(self):
        """Tạo công việc định kỳ mới"""
        self.ensure_one()
        
        if not self.is_recurring:
            return False
        
        # Kiểm tra xem đã đến ngày tạo chưa
        today = fields.Date.today()
        if self.next_recurrence_date and self.next_recurrence_date > today:
            return False
        
        # Kiểm tra xem đã hết thời gian lặp chưa
        if self.recurrence_end_date and today > self.recurrence_end_date:
            return False
        
        # Tính toán ngày cho task mới
        next_date = self._calculate_next_recurrence_date()
        if not next_date:
            return False
        
        # Tính duration (số ngày)
        duration_days = 0
        if self.ngay_ket_thuc and self.ngay_bat_dau:
            duration_days = (self.ngay_ket_thuc - self.ngay_bat_dau).days
        
        # Tạo task mới
        new_task_vals = {
            'ten_cong_viec': self.ten_cong_viec,
            'mo_ta': self.mo_ta,
            'loai_cong_viec': self.loai_cong_viec,
            'du_an_id': self.du_an_id.id,
            'giai_doan': self.giai_doan,
            'nguoi_phu_trach_id': self.nguoi_phu_trach_id.id,
            'nguoi_kiem_tra_id': self.nguoi_kiem_tra_id.id if self.nguoi_kiem_tra_id else False,
            'nguoi_ho_tro_ids': [(6, 0, self.nguoi_ho_tro_ids.ids)],
            'ngay_bat_dau': next_date,
            'ngay_ket_thuc': next_date + timedelta(days=duration_days) if duration_days else next_date,
            'thoi_gian_uoc_tinh': self.thoi_gian_uoc_tinh,
            'do_uu_tien': self.do_uu_tien,
            'do_kho': self.do_kho,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
            'parent_recurring_task_id': self.id,
            'is_recurring': False,  # Task con không phải recurring
        }
        
        # Tạo task
        new_task = self.create(new_task_vals)
        
        # Cập nhật next_recurrence_date cho task gốc
        self.write({
            'next_recurrence_date': self._calculate_next_recurrence_date()
        })
        
        return new_task
    
    @api.model
    def _cron_create_recurring_tasks(self):
        """Cron job: Tạo các công việc định kỳ"""
        recurring_tasks = self.search([
            ('is_recurring', '=', True),
            '|',
            ('recurrence_end_date', '=', False),
            ('recurrence_end_date', '>=', fields.Date.today())
        ])
        
        created_count = 0
        for task in recurring_tasks:
            new_task = task._create_recurring_task()
            if new_task:
                created_count += 1
        
        return created_count

    _sql_constraints = [
        ('ma_cong_viec_unique', 'UNIQUE(ma_cong_viec)', 'Mã công việc phải là duy nhất!'),
        ('check_tien_do', 'CHECK(tien_do >= 0 AND tien_do <= 100)', 'Tiến độ phải từ 0 đến 100!')
    ]


class CongViecTag(models.Model):
    _name = 'cong_viec.tag'
    _description = 'Nhãn công việc'

    name = fields.Char(string='Tên nhãn', required=True)
    color = fields.Integer(string='Màu sắc')
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Tên nhãn phải là duy nhất!')
    ]


class CongViecChecklist(models.Model):
    _name = 'cong_viec.checklist'
    _description = 'Checklist công việc'
    _order = 'sequence, id'

    cong_viec_id = fields.Many2one('cong_viec', string='Công việc', required=True, ondelete='cascade')
    name = fields.Char(string='Nội dung', required=True)
    done = fields.Boolean(string='Hoàn thành', default=False)
    sequence = fields.Integer(string='Thứ tự', default=10)
    
    nguoi_phu_trach_id = fields.Many2one('nhan_vien', string='Người phụ trách')
    ngay_hoan_thanh = fields.Date(string='Ngày hoàn thành')

    @api.onchange('done')
    def _onchange_done(self):
        if self.done:
            self.ngay_hoan_thanh = date.today()
        else:
            self.ngay_hoan_thanh = False


class CongViecTimesheet(models.Model):
    _name = 'cong_viec.timesheet'
    _description = 'Timesheet công việc'
    _order = 'ngay desc'

    cong_viec_id = fields.Many2one('cong_viec', string='Công việc', required=True, ondelete='cascade')
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True)
    
    ngay = fields.Date(string='Ngày', default=fields.Date.today, required=True)
    so_gio = fields.Float(string='Số giờ', required=True)
    mo_ta = fields.Text(string='Mô tả công việc')
    
    du_an_id = fields.Many2one(
        'du_an',
        string='Dự án',
        related='cong_viec_id.du_an_id',
        store=True
    )
