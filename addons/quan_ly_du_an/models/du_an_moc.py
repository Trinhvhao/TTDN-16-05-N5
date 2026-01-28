# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class DuAnMoc(models.Model):
    _name = 'du_an.moc'
    _description = 'Mốc thời gian dự án'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'deadline, is_reached desc, name'

    # ==================== THÔNG TIN CƠ BẢN ====================
    name = fields.Char(string='Tên mốc thời gian', required=True, tracking=True)
    du_an_id = fields.Many2one(
        'du_an',
        string='Dự án',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    description = fields.Html(string='Mô tả chi tiết')
    
    # ==================== THỜI GIAN ====================
    deadline = fields.Date(string='Deadline', tracking=True, required=True)
    is_reached = fields.Boolean(string='Đã đạt được', default=False, tracking=True)
    reached_date = fields.Date(
        string='Ngày đạt được',
        compute='_compute_reached_date',
        store=True,
        readonly=True
    )
    
    # ==================== TÍNH TOÁN ====================
    is_deadline_exceeded = fields.Boolean(
        string='Quá hạn',
        compute='_compute_is_deadline_exceeded',
        store=True
    )
    
    is_deadline_future = fields.Boolean(
        string='Deadline trong tương lai',
        compute='_compute_is_deadline_future',
        store=True
    )
    
    days_remaining = fields.Integer(
        string='Số ngày còn lại',
        compute='_compute_days_remaining',
        store=True
    )
    
    # ==================== KPI & DELIVERABLES ====================
    deliverables = fields.Text(string='Sản phẩm bàn giao')
    success_criteria = fields.Text(string='Tiêu chí thành công')
    
    completion_percentage = fields.Float(
        string='Tiến độ hoàn thành (%)',
        default=0.0,
        tracking=True
    )
    
    # ==================== PHÂN LOẠI ====================
    milestone_type = fields.Selection([
        ('planning', 'Lên kế hoạch'),
        ('design', 'Thiết kế'),
        ('development', 'Phát triển'),
        ('testing', 'Kiểm thử'),
        ('deployment', 'Triển khai'),
        ('review', 'Đánh giá'),
        ('other', 'Khác')
    ], string='Loại mốc', default='other')
    
    priority = fields.Selection([
        ('0', 'Thấp'),
        ('1', 'Trung bình'),
        ('2', 'Cao'),
        ('3', 'Rất cao')
    ], string='Độ ưu tiên', default='1')
    
    # ==================== NGƯỜI PHỤ TRÁCH ====================
    responsible_id = fields.Many2one(
        'nhan_vien',
        string='Người chịu trách nhiệm'
    )
    
    # ==================== KHÁC ====================
    color = fields.Integer(string='Color Index', default=0)
    sequence = fields.Integer(string='Thứ tự', default=10)
    active = fields.Boolean(default=True)
    notes = fields.Text(string='Ghi chú')

    # ==================== COMPUTED METHODS ====================
    @api.depends('is_reached')
    def _compute_reached_date(self):
        """Tự động cập nhật ngày đạt được khi đánh dấu hoàn thành"""
        for record in self:
            if record.is_reached and not record.reached_date:
                record.reached_date = fields.Date.context_today(record)
            elif not record.is_reached:
                record.reached_date = False

    @api.depends('is_reached', 'deadline')
    def _compute_is_deadline_exceeded(self):
        """Kiểm tra xem đã quá deadline chưa"""
        today = fields.Date.context_today(self)
        for record in self:
            if not record.is_reached and record.deadline:
                record.is_deadline_exceeded = record.deadline < today
            else:
                record.is_deadline_exceeded = False

    @api.depends('deadline')
    def _compute_is_deadline_future(self):
        """Kiểm tra deadline có trong tương lai không"""
        today = fields.Date.context_today(self)
        for record in self:
            record.is_deadline_future = record.deadline and record.deadline > today

    @api.depends('deadline', 'is_reached')
    def _compute_days_remaining(self):
        """Tính số ngày còn lại đến deadline"""
        today = fields.Date.context_today(self)
        for record in self:
            if record.deadline and not record.is_reached:
                delta = record.deadline - today
                record.days_remaining = delta.days
            else:
                record.days_remaining = 0

    # ==================== ACTIONS ====================
    def action_mark_reached(self):
        """Đánh dấu mốc đã đạt được"""
        self.write({
            'is_reached': True,
            'completion_percentage': 100.0,
            'reached_date': fields.Date.context_today(self)
        })
        return True

    def action_mark_not_reached(self):
        """Đánh dấu mốc chưa đạt được"""
        self.write({
            'is_reached': False,
            'reached_date': False
        })
        return True

    def toggle_is_reached(self):
        """Toggle trạng thái đã đạt/chưa đạt"""
        self.ensure_one()
        self.is_reached = not self.is_reached
        return self._get_data()

    # ==================== HELPERS ====================
    @api.model
    def _get_fields_to_export(self):
        """Danh sách fields để export"""
        return [
            'id', 'name', 'deadline', 'is_reached', 'reached_date',
            'is_deadline_exceeded', 'is_deadline_future', 'days_remaining',
            'completion_percentage', 'priority'
        ]

    def _get_data(self):
        """Lấy dữ liệu milestone dưới dạng dict"""
        self.ensure_one()
        return {field: self[field] for field in self._get_fields_to_export()}

    def _get_data_list(self):
        """Lấy danh sách milestones dưới dạng list of dict"""
        return [ms._get_data() for ms in self]

    @api.model
    def get_milestones_summary(self, du_an_id):
        """Lấy tổng quan milestones của dự án"""
        milestones = self.search([('du_an_id', '=', du_an_id)])
        total = len(milestones)
        reached = len(milestones.filtered('is_reached'))
        exceeded = len(milestones.filtered('is_deadline_exceeded'))
        
        return {
            'total': total,
            'reached': reached,
            'not_reached': total - reached,
            'exceeded': exceeded,
            'completion_rate': (reached / total * 100) if total > 0 else 0
        }
