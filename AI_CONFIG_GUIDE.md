# Hướng dẫn Cấu hình AI Assistant

## Vấn đề gặp phải
```
WARNING TrinhHao_Odoo odoo.http: Chưa cấu hình AI. Vui lòng vào Cấu hình > AI Config để thiết lập.
```

## Nguyên nhân
Module `ai_assistant` yêu cầu cấu hình API Key để kết nối với dịch vụ AI (OpenRouter, OpenAI, Gemini, v.v.).

## Giải pháp

### Bước 1: Truy cập Cấu hình AI
1. Mở Odoo tại: `http://localhost:8069`
2. Vào menu: **AI Assistant** > **Cấu hình**
3. Hoặc tìm kiếm **"Cấu hình AI"** trên thanh tìm kiếm

### Bước 2: Cấu hình API Key
Hệ thống hỗ trợ các dịch vụ sau:

#### Option 1: OpenRouter AI (Khuyến nghị - Free tier)
- Website: https://openrouter.ai
- Đăng ký tài khoản miễn phí
- Lấy API Key từ: Settings > API Keys
- API URL: `https://openrouter.ai/api/v1/chat/completions`
- Model mặc định: `xiaomi/mimo-v2-flash:free` (hoặc các model khác theo yêu cầu)

#### Option 2: OpenAI
- Website: https://platform.openai.com
- API URL: `https://api.openai.com/v1/chat/completions`
- Model: `gpt-4` hoặc `gpt-3.5-turbo`

#### Option 3: Google Gemini
- Website: https://makersuite.google.com/app/apikey
- API URL: `https://generativelanguage.googleapis.com/v1/models/...`
- Model: `gemini-pro`

### Bước 3: Nhập Thông tin
| Trường | Giá trị | Ghi chú |
|--------|--------|--------|
| **Tên cấu hình** | OpenRouter AI Config | Tên để nhận dạng |
| **API Key** | `sk-or-v1-xxxxx...` | Lấy từ trang Settings của dịch vụ |
| **API URL** | `https://openrouter.ai/api/v1/chat/completions` | URL endpoint |
| **Model** | `xiaomi/mimo-v2-flash:free` | Model AI sử dụng |
| **Max Tokens** | 2048 | Độ dài phản hồi tối đa |
| **Temperature** | 0.7 | Độ sáng tạo (0-1: thấp-cao) |
| **Hoạt động** | ✓ | Bật cấu hình |

### Bước 4: Test Kết nối
1. Nhấn nút **"Test kết nối"** (icon dấu check)
2. Nếu thành công: Xuất hiện thông báo xanh
3. Nếu thất bại: Kiểm tra API Key và URL

### Bước 5: Lưu Cấu hình
- Nhấn **"Lưu"** (Ctrl+S)
- Quay lại và thử lại tính năng AI

## Danh sách Models Hỗ trợ OpenRouter

| Model | Tốc độ | Chi phí | Khuyến nghị |
|-------|--------|--------|------------|
| `xiaomi/mimo-v2-flash:free` | ⚡⚡⚡ | Free | ✅ Mặc định |
| `google/gemini-pro` | ⚡⚡ | Rẻ | Khá tốt |
| `openai/gpt-3.5-turbo` | ⚡⚡ | Rẻ | Chính xác |
| `anthropic/claude-3-opus` | ⚡ | Đắt | Chất lượng cao |
| `meta-llama/llama-2-70b` | ⚡ | Miễn phí | Open source |

## Sử dụng AI Assistant

### Sau khi cấu hình thành công:

1. **Phân tích AI:** AI Assistant > Phân tích AI
2. **Chat với AI:** AI Assistant > Lịch sử Chat
3. **Tích hợp tự động:**
   - Khi tạo nhân viên: AI gợi ý bổ sung thông tin
   - Khi tạo dự án: AI phân tích rủi ro tự động
   - Khi giao việc: AI ước tính thời gian cần thiết

## Troubleshooting

### Lỗi: "API Key không hợp lệ"
- **Nguyên nhân:** API Key sai hoặc hết hạn
- **Giải pháp:** Kiểm tra lại API Key, regenerate nếu cần

### Lỗi: "Connection timeout"
- **Nguyên nhân:** Server bị chậm hoặc mất kết nối
- **Giải pháp:** Kiểm tra internet, thử lại sau vài giây

### Lỗi: "Model not found"
- **Nguyên nhân:** Model name sai hoặc không được hỗ trợ
- **Giải pháp:** Chọn model từ danh sách hỗ trợ ở trên

### Vẫn thấy cảnh báo sau khi cấu hình?
- Làm mới trang: F5 hoặc Ctrl+R
- Logout rồi login lại
- Restart Odoo server

## Liên hệ Hỗ trợ
- Gửi email: support@fitdnu.edu.vn
- GitHub Issues: https://github.com/fitdnu/odoo-fitdnu/issues
