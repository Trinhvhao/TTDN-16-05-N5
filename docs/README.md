# 📋 HỆ THỐNG QUẢN LÝ DOANH NGHIỆP ODOO

## Tổng quan dự án

Hệ thống quản lý doanh nghiệp được xây dựng trên nền tảng **Odoo 15.0**, bao gồm 4 module chính:

| Module | Mô tả | Phụ thuộc |
|--------|-------|-----------|
| `nhan_su` | Quản lý nhân sự | base, mail |
| `quan_ly_du_an` | Quản lý dự án | base, mail, nhan_su |
| `quan_ly_cong_viec` | Quản lý công việc | base, mail, nhan_su, quan_ly_du_an |
| `ai_assistant` | Trợ lý AI | base, mail, nhan_su, quan_ly_du_an, quan_ly_cong_viec |

---

## 🔄 Các cải tiến so với ban đầu

### Vấn đề ban đầu & Giải pháp

| Vấn đề | Giải pháp đã áp dụng |
|--------|----------------------|
| Module quá đơn giản, ít chức năng | Mở rộng đáng kể với nhiều model, field và tính năng mới |
| Lỗi xpath selector dùng `@string` | Sửa thành `@name` theo chuẩn Odoo |
| Thiếu liên kết user với nhân viên | Thêm field `user_id` liên kết với `res.users` |
| Không có tính năng AI | Tích hợp OpenRouter API với model Xiaomi MIMO |
| Thiếu timesheet, checklist | Thêm đầy đủ các tính năng quản lý thời gian |
| Views đơn giản | Thêm Kanban, Calendar, Pivot, Graph views |
| Không có báo cáo | Thêm SQL views cho hiệu suất nhân viên/dự án |

---

## 📁 Module 1: NHÂN SỰ (`nhan_su`)

### Mô tả
Module quản lý toàn diện thông tin nhân viên, phòng ban, chức vụ và hợp đồng lao động.

### Models

#### 1. `nhan_vien` - Nhân viên
**Thông tin cá nhân:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `ma_nhan_vien` | Mã nhân viên (tự động) | Char |
| `ho_ten_dem`, `ten` | Họ tên đệm, Tên | Char |
| `ho_ten` | Họ và tên (computed) | Char |
| `ngay_sinh` | Ngày sinh | Date |
| `tuoi` | Tuổi (computed) | Integer |
| `gioi_tinh` | Giới tính | Selection |
| `cmnd_cccd` | CMND/CCCD | Char |
| `ngay_cap_cmnd`, `noi_cap_cmnd` | Ngày cấp, nơi cấp | Date, Char |
| `quoc_tich` | Quốc tịch | Many2one |
| `dan_toc`, `ton_giao` | Dân tộc, tôn giáo | Char |
| `tinh_trang_hon_nhan` | Tình trạng hôn nhân | Selection |

**Địa chỉ & Liên lạc:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `dia_chi` | Địa chỉ hiện tại | Text |
| `que_quan` | Quê quán | Char |
| `dia_chi_thuong_tru` | Địa chỉ thường trú | Text |
| `tinh_thanh_id` | Tỉnh/Thành phố | Many2one |
| `email`, `email_cong_ty` | Email cá nhân/công ty | Char |
| `dien_thoai` | Số điện thoại | Char |
| `nguoi_lien_he_khan_cap` | Người liên hệ khẩn cấp | Char |
| `dien_thoai_khan_cap` | SĐT khẩn cấp | Char |

**Thông tin công việc:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `phong_ban_id` | Phòng ban | Many2one |
| `chuc_vu_id` | Chức vụ | Many2one |
| `cap_bac` | Cấp bậc (nhân viên → giám đốc) | Selection |
| `ngay_vao_lam` | Ngày vào làm | Date |
| `ngay_chinh_thuc` | Ngày chính thức | Date |
| `tham_nien` | Thâm niên (computed, năm) | Float |
| `loai_hop_dong` | Loại hợp đồng | Selection |
| `trang_thai` | Trạng thái làm việc | Selection |
| `manager_id` | Quản lý trực tiếp | Many2one |
| `user_id` | Tài khoản người dùng | Many2one |

**Lương & Phụ cấp:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `luong_co_ban` | Lương cơ bản | Float |
| `phu_cap_an_trua` | Phụ cấp ăn trưa | Float |
| `phu_cap_di_lai` | Phụ cấp đi lại | Float |
| `phu_cap_dien_thoai` | Phụ cấp điện thoại | Float |
| `phu_cap_khac` | Phụ cấp khác | Float |
| `tong_thu_nhap` | Tổng thu nhập (computed) | Float |
| `so_tai_khoan`, `ngan_hang` | Thông tin ngân hàng | Char |
| `ma_so_thue`, `so_bhxh`, `so_bhyt` | Mã số thuế, BHXH, BHYT | Char |

**Học vấn & Kỹ năng:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `trinh_do_hoc_van` | Trình độ học vấn | Selection |
| `chuyen_nganh` | Chuyên ngành | Char |
| `truong_tot_nghiep` | Trường tốt nghiệp | Char |
| `ky_nang_ids` | Kỹ năng | Many2many |
| `chung_chi_ids` | Chứng chỉ | One2many |
| `ngoai_ngu` | Ngoại ngữ | Char |
| `trinh_do_ngoai_ngu` | Trình độ ngoại ngữ | Selection |

**AI Fields (từ ai_assistant):**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `ai_danh_gia` | Đánh giá từ AI | Text |
| `ai_goi_y_dao_tao` | Gợi ý đào tạo từ AI | Text |
| `ai_updated` | Thời gian AI cập nhật | Datetime |

#### 2. `nhan_vien.ky_nang` - Kỹ năng
| Field | Mô tả |
|-------|-------|
| `name` | Tên kỹ năng |
| `loai_ky_nang` | Loại (kỹ thuật/mềm/quản lý/ngoại ngữ) |
| `color` | Màu hiển thị |

#### 3. `nhan_vien.chung_chi` - Chứng chỉ
| Field | Mô tả |
|-------|-------|
| `ten_chung_chi` | Tên chứng chỉ |
| `to_chuc_cap` | Tổ chức cấp |
| `ngay_cap`, `ngay_het_han` | Ngày cấp, hết hạn |
| `con_hieu_luc` | Còn hiệu lực (computed) |

#### 4. `nhan_vien.nguoi_phu_thuoc` - Người phụ thuộc
| Field | Mô tả |
|-------|-------|
| `ho_ten` | Họ tên |
| `quan_he` | Quan hệ (vợ/chồng, con, cha/mẹ...) |
| `ngay_sinh`, `cmnd_cccd` | Ngày sinh, CMND |

#### 5. `nhan_vien.hop_dong` - Hợp đồng lao động
| Field | Mô tả |
|-------|-------|
| `ma_hop_dong` | Mã hợp đồng (tự động) |
| `loai_hop_dong` | Loại hợp đồng |
| `ngay_bat_dau`, `ngay_ket_thuc` | Thời hạn |
| `luong_co_ban` | Mức lương |
| `trang_thai` | Trạng thái (nháp/hiệu lực/hết hạn) |

#### 6. `phong_ban` - Phòng ban
| Field | Mô tả |
|-------|-------|
| `ma_phong_ban` | Mã phòng ban |
| `ten_phong_ban` | Tên phòng ban |
| `truong_phong_id` | Trưởng phòng |
| `parent_id` | Phòng ban cha |
| `nhan_vien_ids` | Danh sách nhân viên |

#### 7. `chuc_vu` - Chức vụ
| Field | Mô tả |
|-------|-------|
| `ma_chuc_vu` | Mã chức vụ |
| `ten_chuc_vu` | Tên chức vụ |
| `cap_bac` | Cấp bậc |
| `phu_cap` | Phụ cấp chức vụ |

### Views
- ✅ Form view với nhiều tabs (Liên lạc, Lương, Học vấn, Người phụ thuộc, Hợp đồng, AI)
- ✅ Tree view với decoration theo trạng thái
- ✅ Kanban view với avatar
- ✅ Search view với filters và group by
- ✅ Pivot và Graph views cho phân tích

### Actions
| Action | Mô tả |
|--------|-------|
| `action_set_dang_lam` | Xác nhận đang làm việc |
| `action_set_nghi_phep` | Đánh dấu nghỉ phép |
| `action_set_nghi_viec` | Đánh dấu nghỉ việc |
| `action_view_hop_dong` | Xem danh sách hợp đồng |
| `action_view_subordinates` | Xem nhân viên cấp dưới |
| `action_ai_danh_gia` | AI đánh giá nhân viên |
| `action_ai_goi_y_dao_tao` | AI gợi ý đào tạo |

---

## 📁 Module 2: QUẢN LÝ DỰ ÁN (`quan_ly_du_an`)

### Mô tả
Module quản lý dự án với đầy đủ thông tin về timeline, ngân sách, nhân sự và quản lý rủi ro.

### Models

#### 1. `du_an` - Dự án
**Thông tin cơ bản:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `ma_du_an` | Mã dự án (tự động) | Char |
| `ten_du_an` | Tên dự án | Char |
| `mo_ta` | Mô tả chi tiết | Html |
| `loai_du_an` | Loại (nội bộ/khách hàng/nghiên cứu...) | Selection |

**Thời gian:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `ngay_bat_dau` | Ngày bắt đầu | Date |
| `ngay_ket_thuc` | Ngày kết thúc thực tế | Date |
| `ngay_ket_thuc_du_kien` | Ngày kết thúc dự kiến | Date |
| `so_ngay` | Số ngày dự kiến (computed) | Integer |
| `so_ngay_con_lai` | Số ngày còn lại (computed) | Integer |
| `tre_tien_do` | Trễ tiến độ (computed) | Boolean |

**Nhân sự:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `quan_ly_du_an_id` | Quản lý dự án (PM) | Many2one |
| `pho_quan_ly_id` | Phó quản lý | Many2one |
| `phong_ban_id` | Phòng ban phụ trách | Many2one |
| `thanh_vien_ids` | Thành viên tham gia | Many2many |
| `so_thanh_vien` | Số thành viên (computed) | Integer |

**Khách hàng:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `khach_hang_id` | Khách hàng | Many2one (res.partner) |
| `lien_he_khach_hang` | Người liên hệ | Char |
| `email_khach_hang`, `dien_thoai_khach_hang` | Email, SĐT KH | Char |

**Trạng thái & Tiến độ:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `trang_thai` | Trạng thái (mới → hoàn thành) | Selection |
| `do_uu_tien` | Độ ưu tiên | Selection |
| `tien_do` | Tiến độ (%) | Float |
| `muc_do_rui_ro` | Mức độ rủi ro | Selection |

**Ngân sách:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `ngan_sach_du_kien` | Ngân sách dự kiến | Float |
| `ngan_sach_thuc_te` | Ngân sách thực tế | Float |
| `ty_le_ngan_sach` | Tỉ lệ ngân sách (computed) | Float |
| `doanh_thu_du_kien`, `doanh_thu_thuc_te` | Doanh thu | Float |
| `loi_nhuan` | Lợi nhuận (computed) | Float |

**Quan hệ:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `tai_lieu_ids` | Tài liệu dự án | One2many |
| `moc_thoi_gian_ids` | Mốc thời gian | One2many |
| `rui_ro_ids` | Danh sách rủi ro | One2many |
| `cong_viec_ids` | Công việc (từ quan_ly_cong_viec) | One2many |

**AI Fields:**
| Field | Mô tả |
|-------|-------|
| `ai_phan_tich_rui_ro` | Phân tích rủi ro AI |
| `ai_goi_y_timeline` | Gợi ý timeline AI |
| `ai_tom_tat` | Tóm tắt dự án AI |

#### 2. `du_an.tag` - Tags dự án
| Field | Mô tả |
|-------|-------|
| `name` | Tên tag |
| `color` | Màu sắc |

#### 3. `du_an.tai_lieu` - Tài liệu dự án
| Field | Mô tả |
|-------|-------|
| `ten_tai_lieu` | Tên tài liệu |
| `loai_tai_lieu` | Loại (hợp đồng/báo cáo/thiết kế...) |
| `file`, `file_name` | File đính kèm |
| `nguoi_tao_id`, `ngay_tao` | Người tạo, ngày tạo |
| `phien_ban` | Phiên bản |

#### 4. `du_an.moc` - Mốc thời gian
| Field | Mô tả |
|-------|-------|
| `ten_moc` | Tên mốc |
| `ngay_muc_tieu` | Ngày mục tiêu |
| `ngay_hoan_thanh` | Ngày hoàn thành |
| `trang_thai` | Trạng thái (chưa đạt/đang thực hiện/đã đạt) |
| `nguoi_phu_trach_id` | Người phụ trách |

#### 5. `du_an.rui_ro` - Quản lý rủi ro
| Field | Mô tả |
|-------|-------|
| `ten_rui_ro` | Tên rủi ro |
| `xac_suat` | Xác suất xảy ra |
| `muc_do_anh_huong` | Mức độ ảnh hưởng |
| `bien_phap_phong_ngua` | Biện pháp phòng ngừa |
| `bien_phap_xu_ly` | Biện pháp xử lý |
| `trang_thai` | Trạng thái |

### Views
- ✅ Form view với tabs (Mô tả, Thành viên, Khách hàng, Mốc, Rủi ro, Tài liệu, AI)
- ✅ Tree view với decoration
- ✅ Kanban view group by trạng thái
- ✅ Calendar view (theo ngày bắt đầu → kết thúc)
- ✅ Pivot và Graph views

### Actions
| Action | Mô tả |
|--------|-------|
| `action_len_ke_hoach` | Chuyển sang lên kế hoạch |
| `action_bat_dau` | Bắt đầu dự án |
| `action_tam_dung` | Tạm dừng |
| `action_hoan_thanh` | Hoàn thành (tien_do = 100%) |
| `action_huy_bo` | Hủy bỏ |
| `action_mo_lai` | Mở lại dự án |
| `action_ai_phan_tich_rui_ro` | AI phân tích rủi ro |
| `action_ai_goi_y_timeline` | AI gợi ý timeline |
| `action_ai_tom_tat` | AI tóm tắt dự án |

---

## 📁 Module 3: QUẢN LÝ CÔNG VIỆC (`quan_ly_cong_viec`)

### Mô tả
Module quản lý công việc/tác vụ với Kanban board, timesheet tracking, checklist và báo cáo hiệu suất.

### Models

#### 1. `cong_viec` - Công việc
**Thông tin cơ bản:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `ma_cong_viec` | Mã công việc (tự động) | Char |
| `ten_cong_viec` | Tên công việc | Char |
| `mo_ta` | Mô tả chi tiết | Html |
| `loai_cong_viec` | Loại (task/bug/feature/improvement...) | Selection |
| `du_an_id` | Dự án | Many2one |
| `giai_doan` | Giai đoạn (phân tích → bảo trì) | Selection |

**Phân công:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `nguoi_phu_trach_id` | Người phụ trách | Many2one |
| `nguoi_tao_id` | Người tạo | Many2one |
| `nguoi_kiem_tra_id` | Người kiểm tra | Many2one |
| `nguoi_ho_tro_ids` | Người hỗ trợ | Many2many |

**Thời gian:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `ngay_bat_dau` | Ngày bắt đầu | Date |
| `ngay_ket_thuc` | Deadline | Date |
| `ngay_hoan_thanh_thuc_te` | Ngày hoàn thành thực tế | Date |
| `thoi_gian_uoc_tinh` | Thời gian ước tính (giờ) | Float |
| `thoi_gian_thuc_te` | Thời gian thực tế (giờ) | Float |
| `hieu_suat` | Hiệu suất (computed) | Float |
| `so_ngay_con_lai` | Số ngày còn lại (computed) | Integer |
| `tre_han` | Trễ hạn (computed) | Boolean |

**Trạng thái:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `trang_thai` | Trạng thái (backlog → hoàn thành) | Selection |
| `do_uu_tien` | Độ ưu tiên (1-4) | Selection |
| `tien_do` | Tiến độ (0-100%) | Float |
| `do_kho` | Độ khó | Selection |

**Công việc con:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `parent_id` | Công việc cha | Many2one |
| `child_ids` | Công việc con | One2many |
| `so_cong_viec_con` | Số công việc con (computed) | Integer |

**Checklist & Timesheet:**
| Field | Mô tả | Kiểu |
|-------|-------|------|
| `checklist_ids` | Danh sách checklist | One2many |
| `tien_do_checklist` | Tiến độ checklist (computed) | Float |
| `gio_lam_viec_ids` | Log giờ làm việc | One2many |
| `tong_gio_log` | Tổng giờ logged (computed) | Float |

**AI Fields:**
| Field | Mô tả |
|-------|-------|
| `ai_uoc_tinh_thoi_gian` | Ước tính thời gian AI |
| `ai_goi_y_thuc_hien` | Gợi ý thực hiện AI |
| `ai_mo_ta_tu_dong` | Mô tả tự động AI |

#### 2. `cong_viec.tag` - Nhãn công việc
| Field | Mô tả |
|-------|-------|
| `name` | Tên nhãn |
| `color` | Màu sắc |

#### 3. `cong_viec.checklist` - Checklist
| Field | Mô tả |
|-------|-------|
| `name` | Nội dung |
| `done` | Đã hoàn thành |
| `sequence` | Thứ tự |
| `nguoi_phu_trach_id` | Người phụ trách |
| `ngay_hoan_thanh` | Ngày hoàn thành |

#### 4. `cong_viec.timesheet` - Timesheet
| Field | Mô tả |
|-------|-------|
| `cong_viec_id` | Công việc |
| `nhan_vien_id` | Nhân viên |
| `ngay` | Ngày làm |
| `so_gio` | Số giờ |
| `mo_ta` | Mô tả công việc đã làm |

#### 5. `hieu_suat_nhan_vien` - Báo cáo hiệu suất nhân viên (SQL View)
| Field | Mô tả |
|-------|-------|
| `nhan_vien_id` | Nhân viên |
| `tong_cong_viec` | Tổng số công việc |
| `cong_viec_hoan_thanh` | Số công việc hoàn thành |
| `cong_viec_tre_han` | Số công việc trễ hạn |
| `ty_le_hoan_thanh` | Tỉ lệ hoàn thành (%) |
| `ty_le_dung_han` | Tỉ lệ đúng hạn (%) |

#### 6. `hieu_suat_du_an` - Báo cáo hiệu suất dự án (SQL View)
| Field | Mô tả |
|-------|-------|
| `du_an_id` | Dự án |
| `tong_cong_viec` | Tổng số công việc |
| `tien_do_trung_binh` | Tiến độ trung bình |
| `ty_le_hoan_thanh` | Tỉ lệ hoàn thành |

### Views
- ✅ Form view với tabs (Mô tả, Checklist, Timesheet, Công việc con, AI)
- ✅ Tree view với decoration theo trạng thái/trễ hạn
- ✅ Kanban view group by trạng thái (Scrum board)
- ✅ Calendar view
- ✅ Pivot và Graph views

### Actions
| Action | Mô tả |
|--------|-------|
| `action_chua_lam` | Đánh dấu sẵn sàng |
| `action_bat_dau` | Bắt đầu làm |
| `action_review` | Gửi review |
| `action_cho_kiem_tra` | Gửi kiểm tra |
| `action_hoan_thanh` | Hoàn thành |
| `action_huy_bo` | Hủy bỏ |
| `action_mo_lai` | Mở lại |
| `action_view_subtasks` | Xem công việc con |
| `action_log_time` | Log giờ làm việc |
| `action_ai_uoc_tinh_thoi_gian` | AI ước tính thời gian |
| `action_ai_goi_y_thuc_hien` | AI gợi ý thực hiện |
| `action_ai_tao_mo_ta` | AI tạo mô tả |
| `action_ai_tao_checklist` | AI tạo checklist tự động |

---

## 📁 Module 4: AI ASSISTANT (`ai_assistant`)

### Mô tả
Module tích hợp AI thông qua OpenRouter API, hỗ trợ phân tích và gợi ý cho tất cả các module khác.

### Cấu hình
| Tham số | Giá trị mặc định |
|---------|------------------|
| API URL | `https://openrouter.ai/api/v1/chat/completions` |
| Model | `xiaomi/mimo-v2-flash:free` |
| Max Tokens | 2048 |
| Temperature | 0.7 |

### Models

#### 1. `ai.config` - Cấu hình AI
| Field | Mô tả |
|-------|-------|
| `api_key` | API Key (OpenRouter) |
| `api_url` | URL endpoint |
| `model` | Tên model |
| `max_tokens` | Số token tối đa |
| `temperature` | Độ sáng tạo (0-1) |
| `system_prompt` | Prompt hệ thống |

**Methods:**
- `call_ai(prompt, system_prompt, context_data)` - Gọi API
- `test_connection()` - Test kết nối

#### 2. `ai.chat` - Phiên chat
| Field | Mô tả |
|-------|-------|
| `user_id` | Người dùng |
| `res_model`, `res_id` | Liên kết record |
| `message_ids` | Danh sách tin nhắn |

#### 3. `ai.chat.message` - Tin nhắn
| Field | Mô tả |
|-------|-------|
| `role` | Vai trò (user/assistant/system) |
| `content` | Nội dung |
| `is_error` | Là lỗi |

### Wizards

#### 1. `ai.quick.ask.wizard` - Hỏi nhanh AI
Cho phép người dùng đặt câu hỏi nhanh cho AI với ngữ cảnh từ record hiện tại.

#### 2. `ai.analysis.wizard` - Phân tích AI
Phân tích tổng hợp dữ liệu:
- Phân tích nhân viên
- Phân tích dự án
- Phân tích công việc
- Phân tích tổng hợp (tất cả)

### Tính năng AI theo module

#### Nhân sự:
| Tính năng | Mô tả |
|-----------|-------|
| **AI Đánh giá** | Đánh giá tổng quan: điểm mạnh, điểm yếu, thang điểm 1-10 |
| **AI Đào tạo** | Gợi ý kỹ năng cần học, khóa học, lộ trình phát triển |

#### Dự án:
| Tính năng | Mô tả |
|-----------|-------|
| **AI Rủi ro** | Xác định rủi ro tiềm ẩn, đánh giá mức độ, đề xuất biện pháp |
| **AI Timeline** | Gợi ý các giai đoạn, mốc milestone, checkpoint |
| **AI Tóm tắt** | Tóm tắt tình trạng, dự báo khả năng hoàn thành |

#### Công việc:
| Tính năng | Mô tả |
|-----------|-------|
| **AI Thời gian** | Ước tính thời gian, các bước thực hiện |
| **AI Gợi ý** | Best practices, lỗi cần tránh |
| **AI Checklist** | Tự động tạo checklist các bước cần làm |

---

## 🔒 Bảo mật & Quyền truy cập

Tất cả các model đều có quyền CRUD đầy đủ cho `base.group_user`.

### Các SQL Constraints:
- `ma_nhan_vien` phải unique
- `cmnd_cccd` phải unique
- `ma_du_an` phải unique
- `ma_cong_viec` phải unique
- `tien_do` phải từ 0-100

---

## 📊 Các Views đặc biệt

### SQL Views (Báo cáo)

#### `hieu_suat_nhan_vien`
```sql
SELECT
    nv.id as nhan_vien_id,
    COUNT(cv.id) as tong_cong_viec,
    COUNT(CASE WHEN cv.trang_thai = 'hoan_thanh' THEN 1 END) as cong_viec_hoan_thanh,
    ROUND(ty_le_hoan_thanh, 2) as ty_le_hoan_thanh,
    ...
FROM nhan_vien nv
LEFT JOIN cong_viec cv ON cv.nguoi_phu_trach_id = nv.id
GROUP BY nv.id
```

#### `hieu_suat_du_an`
```sql
SELECT
    da.id as du_an_id,
    COUNT(cv.id) as tong_cong_viec,
    AVG(cv.tien_do) as tien_do_trung_binh,
    ...
FROM du_an da
LEFT JOIN cong_viec cv ON cv.du_an_id = da.id
GROUP BY da.id
```

---

## 🎨 UI/UX Features

| Tính năng | Mô tả |
|-----------|-------|
| **Statusbar** | Hiển thị trạng thái dạng workflow |
| **Progressbar** | Hiển thị tiến độ dạng thanh |
| **Priority widget** | Hiển thị độ ưu tiên dạng sao |
| **Ribbon** | Hiển thị cảnh báo trễ hạn |
| **Decoration** | Màu sắc theo trạng thái |
| **Kanban** | Board view kéo thả |
| **Calendar** | Lịch công việc/dự án |
| **Stat buttons** | Button thống kê nhanh |
| **Chatter** | Message log, activity |

---

## 📝 Sequences (Mã tự động)

| Model | Prefix | Ví dụ |
|-------|--------|-------|
| Nhân viên | NV | NV00001 |
| Hợp đồng | HD | HD00001 |
| Dự án | DA | DA00001 |
| Công việc | CV | CV00001 |

---

## 🚀 Hướng dẫn sử dụng

### 1. Cài đặt
```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt modules
python3 odoo-bin.py -c odoo.conf -d odoo -i nhan_su,quan_ly_du_an,quan_ly_cong_viec,ai_assistant --stop-after-init

# Chạy server
python3 odoo-bin.py -c odoo.conf -d odoo
```

### 2. Cấu hình AI
1. Đăng nhập Odoo
2. Vào menu **AI Assistant > Cấu hình**
3. Tạo cấu hình mới với API Key từ [OpenRouter](https://openrouter.ai/)
4. Bấm **Test kết nối** để kiểm tra

### 3. Sử dụng
- **Nhân sự**: Quản lý nhân viên, hợp đồng, đánh giá AI
- **Dự án**: Tạo dự án, quản lý timeline, phân tích rủi ro AI
- **Công việc**: Kanban board, timesheet, checklist AI

---

## 📌 Tóm tắt cải tiến

| Khía cạnh | Trước | Sau |
|-----------|-------|------|
| **Số model** | ~5 | 20+ |
| **Số field** | ~30 | 200+ |
| **Views** | Form, Tree | Form, Tree, Kanban, Calendar, Pivot, Graph |
| **AI** | Không có | Tích hợp OpenRouter |
| **Timesheet** | Không có | Có |
| **Checklist** | Không có | Có |
| **Báo cáo** | Không có | SQL Views |
| **Rủi ro** | Không có | Quản lý đầy đủ |
| **Tài liệu** | Không có | Upload/quản lý |

---

**Phiên bản:** 15.0.1.0.0  
**Tác giả:** FITDNU  
**Cập nhật:** 28/01/2026
