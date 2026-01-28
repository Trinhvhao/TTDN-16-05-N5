# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import json


class NhanVienAI(models.Model):
    """Mở rộng Nhân viên với tính năng AI"""
    _inherit = 'nhan_vien'

    ai_danh_gia = fields.Text(string='Đánh giá AI', readonly=True)
    ai_goi_y_dao_tao = fields.Text(string='Gợi ý đào tạo AI', readonly=True)
    ai_updated = fields.Datetime(string='AI cập nhật lúc', readonly=True)

    def action_ai_danh_gia(self):
        """Yêu cầu AI đánh giá nhân viên"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        # Thu thập dữ liệu nhân viên
        data = {
            'ho_ten': self.ho_ten,
            'chuc_vu': self.chuc_vu_id.name if self.chuc_vu_id else '',
            'phong_ban': self.phong_ban_id.name if self.phong_ban_id else '',
            'tham_nien': self.tham_nien,
            'trinh_do_hoc_van': dict(self._fields['trinh_do_hoc_van'].selection).get(self.trinh_do_hoc_van, ''),
            'ky_nang': [k.name for k in self.ky_nang_ids],
            'chung_chi': [c.ten_chung_chi for c in self.chung_chi_ids],
        }
        
        # Thu thập thông tin công việc nếu có
        if hasattr(self, 'cong_viec_ids') and self.cong_viec_ids:
            cong_viec_data = []
            for cv in self.cong_viec_ids[:10]:  # Giới hạn 10 công việc gần nhất
                cong_viec_data.append({
                    'ten': cv.ten_cong_viec,
                    'trang_thai': cv.trang_thai,
                    'tien_do': cv.tien_do,
                    'tre_han': cv.tre_han
                })
            data['cong_viec_gan_day'] = cong_viec_data
        
        prompt = f"""Hãy đánh giá tổng quan nhân viên này dựa trên thông tin được cung cấp.
Đưa ra:
1. Điểm mạnh
2. Điểm cần cải thiện  
3. Đánh giá tổng thể (thang điểm 1-10)
4. Nhận xét ngắn gọn

Thông tin nhân viên:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            self.write({
                'ai_danh_gia': result,
                'ai_updated': fields.Datetime.now()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': 'Đã hoàn thành đánh giá AI',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(str(e))

    def action_ai_goi_y_dao_tao(self):
        """Yêu cầu AI gợi ý đào tạo cho nhân viên"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        data = {
            'ho_ten': self.ho_ten,
            'chuc_vu': self.chuc_vu_id.name if self.chuc_vu_id else '',
            'cap_bac': dict(self._fields['cap_bac'].selection).get(self.cap_bac, ''),
            'ky_nang_hien_tai': [k.name for k in self.ky_nang_ids],
            'trinh_do_ngoai_ngu': dict(self._fields['trinh_do_ngoai_ngu'].selection).get(self.trinh_do_ngoai_ngu, '') if self.trinh_do_ngoai_ngu else '',
            'chuyen_nganh': self.chuyen_nganh or '',
        }
        
        prompt = f"""Dựa trên thông tin nhân viên, hãy gợi ý lộ trình đào tạo phù hợp:
1. Các kỹ năng cần học thêm
2. Các khóa học/chứng chỉ nên có
3. Lộ trình phát triển nghề nghiệp trong 1-2 năm tới
4. Các nguồn học tập gợi ý (online courses, sách, v.v.)

Thông tin:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            self.write({
                'ai_goi_y_dao_tao': result,
                'ai_updated': fields.Datetime.now()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': 'Đã nhận gợi ý đào tạo từ AI',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(str(e))


class DuAnAI(models.Model):
    """Mở rộng Dự án với tính năng AI"""
    _inherit = 'du_an'

    ai_phan_tich_rui_ro = fields.Text(string='Phân tích rủi ro AI', readonly=True)
    ai_goi_y_timeline = fields.Text(string='Gợi ý Timeline AI', readonly=True)
    ai_tom_tat = fields.Text(string='Tóm tắt dự án AI', readonly=True)
    ai_updated = fields.Datetime(string='AI cập nhật lúc', readonly=True)

    def action_ai_phan_tich_rui_ro(self):
        """AI phân tích rủi ro dự án"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        data = {
            'ten_du_an': self.ten_du_an,
            'loai_du_an': dict(self._fields['loai_du_an'].selection).get(self.loai_du_an, ''),
            'ngay_bat_dau': str(self.ngay_bat_dau) if self.ngay_bat_dau else '',
            'ngay_ket_thuc_du_kien': str(self.ngay_ket_thuc_du_kien) if self.ngay_ket_thuc_du_kien else '',
            'so_thanh_vien': self.so_thanh_vien,
            'ngan_sach_du_kien': self.ngan_sach_du_kien,
            'tien_do_hien_tai': self.tien_do,
            'tre_tien_do': self.tre_tien_do,
            'mo_ta': self.mo_ta_ngan or '',
        }
        
        # Thêm thông tin rủi ro hiện tại
        if self.rui_ro_ids:
            data['rui_ro_da_xac_dinh'] = [
                {'ten': r.ten_rui_ro, 'muc_do': r.muc_do_anh_huong, 'trang_thai': r.trang_thai}
                for r in self.rui_ro_ids
            ]
        
        prompt = f"""Phân tích rủi ro cho dự án này và đề xuất biện pháp phòng ngừa:
1. Xác định các rủi ro tiềm ẩn (kỹ thuật, nhân sự, thời gian, ngân sách)
2. Đánh giá mức độ nghiêm trọng (cao/trung bình/thấp)
3. Đề xuất biện pháp giảm thiểu cụ thể
4. Khuyến nghị ưu tiên

Thông tin dự án:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            self.write({
                'ai_phan_tich_rui_ro': result,
                'ai_updated': fields.Datetime.now()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': 'Đã phân tích rủi ro dự án',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(str(e))

    def action_ai_goi_y_timeline(self):
        """AI gợi ý timeline dự án"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        data = {
            'ten_du_an': self.ten_du_an,
            'loai_du_an': dict(self._fields['loai_du_an'].selection).get(self.loai_du_an, ''),
            'so_ngay_du_kien': self.so_ngay,
            'so_thanh_vien': self.so_thanh_vien,
            'mo_ta': self.mo_ta_ngan or '',
        }
        
        # Thêm mốc thời gian hiện tại
        if self.moc_thoi_gian_ids:
            data['moc_hien_tai'] = [
                {'ten': m.ten_moc, 'ngay': str(m.ngay_muc_tieu), 'trang_thai': m.trang_thai}
                for m in self.moc_thoi_gian_ids
            ]
        
        prompt = f"""Gợi ý timeline và các mốc quan trọng cho dự án:
1. Các giai đoạn chính cần có
2. Thời gian ước tính cho mỗi giai đoạn
3. Các mốc milestone quan trọng
4. Điểm kiểm tra (checkpoint) nên đặt

Thông tin dự án:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            self.write({
                'ai_goi_y_timeline': result,
                'ai_updated': fields.Datetime.now()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': 'Đã nhận gợi ý timeline từ AI',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(str(e))

    def action_ai_tom_tat(self):
        """AI tóm tắt dự án"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        data = {
            'ten_du_an': self.ten_du_an,
            'trang_thai': dict(self._fields['trang_thai'].selection).get(self.trang_thai, ''),
            'tien_do': self.tien_do,
            'so_thanh_vien': self.so_thanh_vien,
            'ngan_sach_du_kien': self.ngan_sach_du_kien,
            'ngan_sach_thuc_te': self.ngan_sach_thuc_te,
            'so_ngay_con_lai': self.so_ngay_con_lai,
            'mo_ta': self.mo_ta_ngan or '',
        }
        
        # Thêm thống kê công việc nếu có
        if hasattr(self, 'cong_viec_ids') and self.cong_viec_ids:
            data['thong_ke_cong_viec'] = {
                'tong': len(self.cong_viec_ids),
                'hoan_thanh': len(self.cong_viec_ids.filtered(lambda x: x.trang_thai == 'hoan_thanh')),
                'dang_lam': len(self.cong_viec_ids.filtered(lambda x: x.trang_thai == 'dang_lam')),
                'tre_han': len(self.cong_viec_ids.filtered(lambda x: x.tre_han))
            }
        
        prompt = f"""Tóm tắt tình trạng dự án hiện tại:
1. Tổng quan tiến độ
2. Những điểm đáng chú ý
3. Vấn đề cần giải quyết
4. Dự báo về khả năng hoàn thành đúng hạn

Thông tin:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            self.write({
                'ai_tom_tat': result,
                'ai_updated': fields.Datetime.now()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': 'Đã tóm tắt dự án',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(str(e))


class CongViecAI(models.Model):
    """Mở rộng Công việc với tính năng AI"""
    _inherit = 'cong_viec'

    ai_uoc_tinh_thoi_gian = fields.Text(string='Ước tính thời gian AI', readonly=True)
    ai_goi_y_thuc_hien = fields.Text(string='Gợi ý thực hiện AI', readonly=True)
    ai_mo_ta_tu_dong = fields.Html(string='Mô tả AI tạo', readonly=True)
    ai_updated = fields.Datetime(string='AI cập nhật lúc', readonly=True)

    def action_ai_uoc_tinh_thoi_gian(self):
        """AI ước tính thời gian hoàn thành"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        data = {
            'ten_cong_viec': self.ten_cong_viec,
            'loai': dict(self._fields['loai_cong_viec'].selection).get(self.loai_cong_viec, ''),
            'do_kho': dict(self._fields['do_kho'].selection).get(self.do_kho, ''),
            'mo_ta': self.mo_ta or '',
            'du_an': self.du_an_id.ten_du_an if self.du_an_id else '',
        }
        
        # Thêm checklist nếu có
        if self.checklist_ids:
            data['checklist'] = [c.name for c in self.checklist_ids]
        
        prompt = f"""Ước tính thời gian hoàn thành công việc này:
1. Thời gian ước tính (giờ/ngày)
2. Các bước thực hiện chính
3. Yếu tố có thể ảnh hưởng thời gian
4. Gợi ý tối ưu để hoàn thành nhanh hơn

Thông tin công việc:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            self.write({
                'ai_uoc_tinh_thoi_gian': result,
                'ai_updated': fields.Datetime.now()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': 'Đã ước tính thời gian công việc',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(str(e))

    def action_ai_goi_y_thuc_hien(self):
        """AI gợi ý cách thực hiện công việc"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        data = {
            'ten_cong_viec': self.ten_cong_viec,
            'loai': dict(self._fields['loai_cong_viec'].selection).get(self.loai_cong_viec, ''),
            'giai_doan': dict(self._fields['giai_doan'].selection).get(self.giai_doan, ''),
            'mo_ta': self.mo_ta or '',
        }
        
        prompt = f"""Gợi ý cách thực hiện công việc hiệu quả:
1. Các bước thực hiện chi tiết
2. Công cụ/tài nguyên nên sử dụng
3. Best practices
4. Những lỗi thường gặp cần tránh
5. Checklist kiểm tra khi hoàn thành

Thông tin:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            self.write({
                'ai_goi_y_thuc_hien': result,
                'ai_updated': fields.Datetime.now()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': 'Đã nhận gợi ý thực hiện từ AI',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(str(e))

    def action_ai_tao_mo_ta(self):
        """AI tạo mô tả chi tiết công việc"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        data = {
            'ten_cong_viec': self.ten_cong_viec,
            'loai': dict(self._fields['loai_cong_viec'].selection).get(self.loai_cong_viec, ''),
            'du_an': self.du_an_id.ten_du_an if self.du_an_id else '',
        }
        
        prompt = f"""Tạo mô tả chi tiết cho công việc này (viết bằng HTML đơn giản):
- Mục tiêu
- Phạm vi công việc
- Yêu cầu đầu vào
- Kết quả đầu ra mong đợi
- Tiêu chí hoàn thành (Definition of Done)

Thông tin:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            self.write({
                'ai_mo_ta_tu_dong': result,
                'ai_updated': fields.Datetime.now()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': 'Đã tạo mô tả công việc',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(str(e))

    def action_ai_tao_checklist(self):
        """AI tạo checklist cho công việc"""
        self.ensure_one()
        
        config = self.env['ai.config'].get_default_config()
        
        data = {
            'ten_cong_viec': self.ten_cong_viec,
            'loai': dict(self._fields['loai_cong_viec'].selection).get(self.loai_cong_viec, ''),
            'mo_ta': self.mo_ta or '',
        }
        
        prompt = f"""Tạo checklist các bước cần làm cho công việc này.
Trả về dưới dạng danh sách, mỗi dòng là một item, ví dụ:
- Bước 1: Làm ABC
- Bước 2: Kiểm tra XYZ
...

Chỉ trả về danh sách, không giải thích thêm.

Thông tin:
{json.dumps(data, ensure_ascii=False, indent=2)}"""

        try:
            result = config.call_ai(prompt)
            
            # Parse kết quả và tạo checklist
            lines = result.strip().split('\n')
            sequence = 10
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('*') or line[0].isdigit()):
                    # Xóa ký tự đầu dòng
                    clean_line = line.lstrip('-*0123456789.).： ').strip()
                    if clean_line:
                        self.env['cong_viec.checklist'].create({
                            'cong_viec_id': self.id,
                            'name': clean_line,
                            'sequence': sequence
                        })
                        sequence += 10
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công!',
                    'message': 'Đã tạo checklist từ AI',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(str(e))
