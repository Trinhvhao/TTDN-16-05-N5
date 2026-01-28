from odoo import fields, models

class Chart(models.Model):
    _name = 'chart'
    _description = 'Biểu đồ tiến độ dự án'

    projects_id = fields.Many2one('projects', string='Tiến độ dự án')