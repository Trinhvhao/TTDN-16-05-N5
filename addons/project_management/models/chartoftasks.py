from odoo import fields, models, api

class ChartOfTasks(models.Model):
    _name = 'chartoftasks'
    _description = 'Biểu đồ tiến độ công việc'

    taskss_id = fields.Many2one('taskss', string='Tiến độ công việc')
