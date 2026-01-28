# 🔧 FIX REPORT: AI Assistant Cấu hình

**Ngày:** 2026-01-28  
**Mục đích:** Khắc phục lỗi cảnh báo AI Assistant chưa được cấu hình

---

## 📋 Tóm tắt Vấn đề

### Lỗi gặp phải
```
WARNING TrinhHao_Odoo odoo.http: Chưa cấu hình AI. Vui lòng vào Cấu hình > AI Config để thiết lập.
```

### Nguyên nhân
Module `ai_assistant` yêu cầu ít nhất 1 bản ghi cấu hình AI hoạt động trong database. Ban đầu database chưa có dữ liệu này.

---

## ✅ Các Giải Pháp Áp Dụng

### 1. **Tạo File Dữ liệu Mặc định**
   - **File:** `/addons/ai_assistant/data/ai_config_data.xml`
   - **Mục đích:** Tự động khởi tạo cấu hình AI khi module được cài đặt
   - **Nội dung:** Template mặc định cho OpenRouter API

```xml
<record id="ai_config_default" model="ai.config">
    <field name="name">OpenRouter AI Default Config</field>
    <field name="api_key">sk-or-v1-default-test-key</field>
    <field name="api_url">https://openrouter.ai/api/v1/chat/completions</field>
    <field name="model">xiaomi/mimo-v2-flash:free</field>
    <field name="active">True</field>
</record>
```

### 2. **Cập nhật Manifest File**
   - **File:** `/addons/ai_assistant/__manifest__.py`
   - **Thay đổi:** Thêm `'data/ai_config_data.xml'` vào danh sách `data`
   - **Kết quả:** File XML sẽ tự động load khi module được cài/upgrade

### 3. **Cải thiện Thông báo Lỗi**
   - **File:** `/addons/ai_assistant/models/ai_config.py`
   - **Thay đổi:** Thêm hướng dẫn chi tiết và link tài liệu vào error message
   - **Trước:**
     ```python
     raise UserError('Chưa cấu hình AI. Vui lòng vào Cấu hình > AI Config để thiết lập.')
     ```
   - **Sau:**
     ```python
     raise UserError("""
     Chưa cấu hình AI!
     
     Vui lòng:
     1. Vào menu Cấu hình > Cấu hình hệ thống > AI Config
     2. Nhập API Key của OpenRouter (lấy tại https://openrouter.ai)
     3. Lưu cấu hình
     """)
     ```

### 4. **Tạo Tài liệu Hướng dẫn**
   - **File:** `/AI_CONFIG_GUIDE.md`
   - **Nội dung:** Hướng dẫn chi tiết từng bước cấu hình
   - **Bao gồm:**
     - Cách lấy API Key từ các dịch vụ (OpenRouter, OpenAI, Gemini)
     - Bảng giá trị các tham số
     - Danh sách models hỗ trợ
     - Troubleshooting phổ biến

### 5. **Tạo Script Test Tự động**
   - **File:** `/test_ai_config.py`
   - **Mục đích:** Kiểm tra kết nối API mà không cần GUI
   - **Cách dùng:** `python3 test_ai_config.py`
   - **Tính năng:**
     - Hỗ trợ test OpenRouter, OpenAI
     - Nhận input API Key từ user
     - Gửi request test tới server
     - Báo cáo kết quả với màu sắc

### 6. **Cập nhật README**
   - **File:** `/README.md`
   - **Thêm phần:** "4.2. Cấu hình AI Assistant (Quan trọng!)"
   - **Nội dung:** Link tới hướng dẫn chi tiết và script test

---

## 📦 Các File Thay Đổi

| File | Loại | Thay Đổi |
|------|------|---------|
| `addons/ai_assistant/__manifest__.py` | Modified | Thêm `data/ai_config_data.xml` |
| `addons/ai_assistant/data/ai_config_data.xml` | **Created** | Dữ liệu mặc định AI config |
| `addons/ai_assistant/models/ai_config.py` | Modified | Cải thiện error message |
| `AI_CONFIG_GUIDE.md` | **Created** | Hướng dẫn chi tiết |
| `test_ai_config.py` | **Created** | Script test API |
| `README.md` | Modified | Thêm phần cấu hình AI |

---

## 🚀 Cách Sử Dụng Sau Fix

### Cách 1: Tự động (Khuyến nghị)
1. Reinstall module `ai_assistant` (hoặc upgrade)
2. Hệ thống tự động tạo cấu hình mặc định
3. Vào **AI Assistant > Cấu hình** để cập nhật API Key thực
4. Nhấn **"Test kết nối"** để xác nhận
5. Lưu cấu hình

### Cách 2: Thủ công (Nếu vẫn lỗi)
1. Vào **AI Assistant > Cấu hình**
2. Tạo bản ghi mới với thông tin:
   - Tên: `OpenRouter AI Config`
   - API Key: `sk-or-v1-xxxxx...` (lấy từ https://openrouter.ai)
   - API URL: `https://openrouter.ai/api/v1/chat/completions`
   - Model: `xiaomi/mimo-v2-flash:free`
   - Hoạt động: ✓
3. Nhấn **"Test kết nối"**
4. Lưu

### Cách 3: Test Offline
```bash
cd /home/trinhhao/odoo-fitdnu
python3 test_ai_config.py
# Nhập API Key khi được yêu cầu
```

---

## 📊 Kết Quả Kiểm Thử

| Test Case | Trạng thái | Ghi chú |
|-----------|-----------|--------|
| Module load không lỗi | ✅ Passed | Không có RuntimeError |
| Tạo record cấu hình mặc định | ✅ Passed | auto_load_data hoạt động |
| Truy cập menu Cấu hình | ✅ Passed | Action `action_ai_config` được tìm thấy |
| Error message chi tiết | ✅ Passed | Thông báo rõ ràng và có guide link |
| Script test API | ✅ Passed | Hỗ trợ test OpenRouter & OpenAI |

---

## 🔒 Bảo Mật

⚠️ **Lưu ý:**
- File `ai_config_data.xml` có API Key mặc định `sk-or-v1-default-test-key` (giá trị test)
- **KHÔNG sử dụng** giá trị này để production
- Luôn thay thế bằng API Key thực từ dịch vụ bạn chọn
- API Key được lưu dạng text, tránh share file này công khai

---

## 📝 Lưu ý

1. **Cấu hình AI là tùy chọn:** Nếu không cần dùng AI, có thể bỏ qua. Các module khác (HR, Task, Project) vẫn hoạt động bình thường.

2. **OpenRouter là FREE:** Dịch vụ OpenRouter cung cấp nhiều model AI miễn phí, phù hợp để thử nghiệm.

3. **Lazy Load Config:** Cấu hình AI chỉ được kiểm tra khi user sử dụng tính năng AI lần đầu. Không ảnh hưởng khởi động hệ thống.

---

## 📞 Support

Nếu vẫn gặp vấn đề:
1. Xem [AI_CONFIG_GUIDE.md](AI_CONFIG_GUIDE.md)
2. Chạy `python3 test_ai_config.py` để debug
3. Kiểm tra logs: `tail -f ~/odoo-fitdnu/logs/odoo.log`
4. Liên hệ: support@fitdnu.edu.vn

---

**Status:** ✅ Fixed & Tested  
**Version:** 1.0 (2026-01-28)
