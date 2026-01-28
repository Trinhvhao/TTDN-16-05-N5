from odoo import models, fields, api

class Budgets(models.Model):
    _name = 'budgets'
    _description = 'Ngân sách dự án'

    budgets_id = fields.Char('Mã ngân sách', required=True)
    budgets_name = fields.Char(string="Tên Ngân Sách")
    projects_id = fields.Many2one('projects', string='Dự Án')

    # total_budget = fields.Float(string='Ngân Sách Dự Án', required=True)
    # actual_expense = fields.Float(string='Chi Phí Thực Tế', compute='_compute_expense')

    expense_ids = fields.One2many('expenses', 'budgets_id', string='Chi Phí')

    budget_planned = fields.Float(string="Ngân sách Dự toán", required=True)
    budget_allocated = fields.Float(string="Ngân sách Phân bổ", required=True)
    budget_reserved = fields.Float(string="Ngân sách Dự trù")
    budget_spent = fields.Float(string="Chi phí Thực tế", compute="_compute_budget_spent", store=True)
    budget_difference = fields.Float(string="Chênh lệch Ngân sách", compute="_compute_budget_difference", store=True)


    @api.depends('expense_ids.amount')  # Sửa lại depend field
    def _compute_budget_spent(self):
        for record in self:
            record.budget_spent = sum(record.expense_ids.mapped('amount'))



    @api.depends('budget_planned', 'budget_spent')
    def _compute_budget_difference(self):
        #Tính toán chênh lệch ngân sách
        for record in self:
            record.budget_difference = record.budget_planned - record.budget_spent

    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.budgets_name}"
            result.append((record.id, name))
        return result