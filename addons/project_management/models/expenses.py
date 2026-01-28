from odoo import models, fields

class Expenses(models.Model):
    _name = 'expenses'
    _description = 'Chi phí thực tế'

    expenses_name = fields.Char(string="Tên Khoản Chi", required=True)
    # projects_id = fields.Many2one('projects', string="Dự án", ondelete='cascade')
    taskss_id = fields.Many2one('taskss', string="Công việc")
    budgets_id = fields.Many2one('budgets', string="Ngân sách")
    amount = fields.Float(string="Số tiền", required=True)
    date = fields.Date(string="Ngày chi tiêu", required=True, default=fields.Date.today)

    