from odoo import models, fields, api

class Employees(models.Model):
    _name = 'employees'
    _description = 'Bảng chứa các thành viên tham gia'

    employees_id = fields.Char("Mã định danh", required=True)
    employees_name = fields.Char('Họ và tên', compute='_tinh_ho_va_ten', store=True)
    employees_date_of_birth = fields.Date('Ngày sinh')
    employees_sex = fields.Selection(
        selection=[
            ('nam', 'Nam'),
            ('nu', 'Nữ'),
            ('khac', "Khác"),
        ],
        string="Giới tính"
    )

    # Thiết lập mối quan hệ Many2many với model 'employees'
    # projects_ids = fields.Many2many('projects', string = 'Dự án')
    # Một nhân viên có nhiều công việc
    # taskss_ids = fields.One2many('taskss', inverse_name='assigned_to', string='Công việc được giao')

    employees_hometown = fields.Char('Quê quán')
    employees_email = fields.Char('Email')
    employees_phone_number = fields.Char("Số điện thoại")

    ho_ten_dem = fields.Char("Họ tên đệm")
    ten = fields.Char("Tên")

    @api.depends("ho_ten_dem", "ten")
    def _tinh_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.employees_name = record.ho_ten_dem + ' ' + record.ten

    @api.onchange("ho_ten_dem", "ten")
    def _tinh_ma_dinh_danh(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                chu_cai_dau = ''.join([tu[0][0] for tu in record.ho_ten_dem.lower().split()])
                record.employees_id = record.ten.lower() + chu_cai_dau

    def name_get(self):
        result = []
        for record in self:
            name = record.employees_name
            result.append((record.id, name))
        return result