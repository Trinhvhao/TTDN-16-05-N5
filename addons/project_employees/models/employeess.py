from odoo import models, fields, api

class Employeess(models.Model):
    _name = 'employeess'
    _description = 'Bảng chứa các thành viên tham gia'

    employeess_id = fields.Char("Mã định danh", required=True)
    employeess_name = fields.Char("Họ và tên")

    # projects_ids = fields.Many2many('projects', string = 'Dự án')