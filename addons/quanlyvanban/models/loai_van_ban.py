# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LoaiVanBan(models.Model):
    _name = 'loai_van_ban'
    _description = 'Loại văn bản'
    _rec_name = 'ten_loai_van_ban'
    
    ma_loai_van_ban = fields.Char("Mã loại văn bản", required=True)
    ten_loai_van_ban = fields.Char("Tên loại văn bản", required=True)
    mo_ta = fields.Text("Mô tả")
    
    @api.constrains('ma_loai_van_ban')
    def _check_unique_ma_loai_van_ban(self):
        for record in self:
            if record.ma_loai_van_ban and self.search_count([
                ('ma_loai_van_ban', '=', record.ma_loai_van_ban),
                ('id', '!=', record.id)
            ]):
                raise ValidationError("Mã loại văn bản phải là duy nhất!")
