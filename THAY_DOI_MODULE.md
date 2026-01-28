# Cấu Trúc Menu Module Quản Lý Văn Bản

## Menu Hierarchy

```
📋 Quản Lý Văn Bản (Menu Root)
├── ⚙️ Cấu Hình
│   └── 📑 Loại Văn Bản (action_loai_van_ban)
└── 📄 Văn Bản
    └── 📋 Danh Sách Văn Bản (action_van_ban)
```

## Cấu Hình Models

### 1. van_ban (Văn Bản chính)
- **Số hiệu văn bản**: Định danh duy nhất (số hiệu)
- **Nơi gửi đến**: Văn bản gửi tới những đơn vị/cá nhân nào
- **Nhân sự xử lý**: Nhân viên HR chịu trách nhiệm xử lý (Many2one nhan_vien)
- **Loại văn bản**: Phân loại (Many2one loai_van_ban)
- **Phòng ban chủ trì**: Phòng ban chủ trì xử lý
- **Trạng thái**: new → processing → approved/rejected → completed/archived
- **Hạn xử lý**: Ngày hạn chót
- **Lịch sử xử lý**: Ghi lại tất cả thay đổi trạng thái

### 2. van_ban.dinh_kem (File đính kèm)
- Cho phép đính kèm file văn bản

### 3. van_ban.lich_su (Lịch sử xử lý)
- Tự động ghi lại từng lần thay đổi trạng thái
- Lưu thông tin: người xử lý, thời gian, trạng thái cũ/mới, ghi chú

### 4. loai_van_ban (Loại văn bản)
- Phân loại: Chỉ tiêu, Quy định, Thông báo, v.v.

## Các Views

### Van Ban
- **Tree View**: Danh sách các văn bản
- **Form View**: Chi tiết từng văn bản
- **Kanban View**: Theo dõi trạng thái
- **Search View**: Tìm kiếm, filter, group by

### Actions
- Gửi Duyệt
- Phê Duyệt
- Từ Chối
- Hoàn Tất

## Kết Nối HR Module

### Trực tiếp
- Field `nhan_su_xu_li_id`: Liên kết đến nhân viên xử lý
- Field `phong_ban_chu_tri_id`: Liên kết đến phòng ban

### Gián tiếp
- Có thể xem các văn bản từ form nhân viên
- Có thể xem các văn bản từ form phòng ban

## Wizard

### Xử Lý Văn Bản
- Cho phép thay đổi trạng thái với ghi chú
- Tự động tạo lịch sử
