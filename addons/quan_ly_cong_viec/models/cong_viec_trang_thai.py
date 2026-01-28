# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CongViecTrangThai(models.Model):
    _name = 'cong_viec.trang_thai'
    _description = 'Trạng thái công việc - Stage'
    _order = 'sequence, id'

    name = fields.Char('Tên trạng thái', required=True, translate=True)
    sequence = fields.Integer('Thứ tự', default=10)
    fold = fields.Boolean(
        'Thu gọn trong Kanban',
        help='Trạng thái này sẽ được thu gọn trong view Kanban và không tính vào tiến độ'
    )
    description = fields.Text('Mô tả')
    
    # Link to projects - một stage có thể dùng cho nhiều dự án
    du_an_ids = fields.Many2many(
        'du_an',
        'cong_viec_trang_thai_du_an_rel',
        'trang_thai_id',
        'du_an_id',
        string='Dự án'
    )
    
    # Stage type để phân loại
    stage_type = fields.Selection([
        ('new', 'Mới'),
        ('in_progress', 'Đang thực hiện'),
        ('review', 'Đang review'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Đã hủy')
    ], string='Loại trạng thái', default='in_progress',
       help='Loại trạng thái để tự động tính toán tiến độ')
    
    active = fields.Boolean(default=True)
    
    # Color for kanban
    color = fields.Integer('Màu sắc')
    
    # Constraints
    _sql_constraints = [
        ('name_unique', 'unique(name, stage_type)', 
         'Tên trạng thái phải là duy nhất trong cùng loại!')
    ]
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """
        Read group customization in order to display all the stages in the
        kanban view, even if they are empty
        """
        # Retrieve du_an_id from context
        du_an_id = self.env.context.get('default_du_an_id')
        
        if du_an_id:
            # Tìm stages của dự án này
            search_domain = ['|', ('du_an_ids', '=', False), ('du_an_ids', '=', du_an_id)]
        else:
            # Hiển thị tất cả stages
            search_domain = []
        
        # Thực hiện search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=1)
        return stages.browse(stage_ids)
