# Phân Tích & Lộ Trình Nâng Cấp Module Quản Lý Công Việc & Nhân Sự
## Dựa trên Module Chuẩn của Odoo

**Ngày phân tích:** 2026-01-28  
**Người thực hiện:** AI Assistant  
**Mục tiêu:** Nâng cấp 2 module `quan_ly_cong_viec` và `nhan_su` dựa trên module chuẩn `project` và `hr` của Odoo

---

## 📊 Tổng Quan Hiện Trạng

### Module Hiện Tại

| Module | Tên | Dependencies | Status | Models |
|--------|-----|--------------|--------|--------|
| `quan_ly_cong_viec` | Quản Lý Công Việc | base, mail, nhan_su, quan_ly_du_an | ⚠️ Cần nâng cấp | cong_viec, hieu_suat.* |
| `nhan_su` | Quản Lý Nhân Sự | base, mail | ⚠️ Cần nâng cấp | nhan_vien, phong_ban, chuc_vu, ... |

### Module Odoo Chuẩn Tham Khảo

| Module Odoo | Tên | Mô tả | Tính năng chính |
|-------------|-----|-------|-----------------|
| `project` | Project Management | Quản lý dự án & công việc | Tasks, Stages, Kanban, Gantt, Timesheet, Dependencies |
| `hr` | Employees | Quản lý nhân sự | Employee profiles, Departments, Job positions, Skills |
| `hr_timesheet` | Timesheets | Theo dõi giờ làm | Time tracking, Analytics |
| `hr_skills` | Employee Skills | Quản lý kỹ năng | Skills, Levels, Resumé |
| `hr_contract` | Contracts | Hợp đồng lao động | Contract types, Salary, Benefits |

---

## 🔍 PART 1: PHÂN TÍCH MODULE QUẢN LÝ CÔNG VIỆC

### 1.1. So Sánh Với Odoo Project Module

#### Cấu Trúc Hiện Tại (`quan_ly_cong_viec`)

**Models:**
- `cong_viec` - Công việc chính
- `hieu_suat.nhan_vien` - Hiệu suất nhân viên  
- `hieu_suat.du_an` - Hiệu suất dự án
- `cong_viec.tag` - Tags công việc

**Điểm Mạnh:**
✅ Có tích hợp với module `nhan_su` và `quan_ly_du_an` sẵn  
✅ Có tracking hiệu suất (hieu_suat)  
✅ Có tag system  

**Điểm Yếu:**
❌ Không có Stage/Status workflow như Odoo  
❌ Thiếu Subtasks (công việc con)  
❌ Không có Dependencies (phụ thuộc giữa tasks)  
❌ Thiếu Timesheet tracking  
❌ Không có Recurring tasks  
❌ Thiếu Priority & Rating system  
❌ Không có Views nâng cao (Gantt, Timeline)  

---

#### Odoo Project Module - Tính Năng Nổi Bật

**1. Task Stages (Workflow)**
```python
# project.task.type model
class ProjectTaskType(models.Model):
    _name = 'project.task.type'
    _description = 'Task Stage'
    _order = 'sequence, id'
    
    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean('Folded in Kanban')
    description = fields.Text()
    project_ids = fields.Many2many('project.project')
```

**Lợi ích:**
- Drag & drop trong Kanban
- Customize workflow theo dự án
- Auto-progress tracking

---

**2. Task Dependencies**
```python
# Trong project.task model
depend_on_ids = fields.Many2many(
    'project.task',
    'task_dependencies_rel',
    'task_id',
    'depends_on_id',
    string='Depends on'
)
dependent_ids = fields.Many2many(
    'project.task',
    'task_dependencies_rel',
    'depends_on_id',
    'task_id',
    string='Dependent Tasks'
)
```

**Lợi ích:**
- Critical path analysis
- Gantt chart với dependencies
- Auto-blocking tasks

---

**3. Subtasks**
```python
parent_id = fields.Many2one('project.task', 'Parent Task')
child_ids = fields.One2many('project.task', 'parent_id', 'Subtasks')
subtask_count = fields.Integer(compute='_compute_subtask_count')
```

**Lợi ích:**
- Chia nhỏ công việc phức tạp
- Progress roll-up tự động
- Better organization

---

**4. Time Tracking**
```python
# hr_timesheet integration
timesheet_ids = fields.One2many(
    'account.analytic.line',
    'task_id',
    string='Timesheets'
)
effective_hours = fields.Float(compute='_compute_effective_hours')
total_hours_spent = fields.Float(compute='_compute_hours')
planned_hours = fields.Float('Initially Planned Hours')
remaining_hours = fields.Float(compute='_compute_remaining_hours')
```

**Lợi ích:**
- Track giờ làm thực tế
- So sánh với estimate
- Billing & invoicing

---

**5. Recurring Tasks**
```python
recurrence_id = fields.Many2one('project.task.recurrence')
recurring_task = fields.Boolean()
repeat_interval = fields.Integer()
repeat_unit = fields.Selection([
    ('day', 'Days'),
    ('week', 'Weeks'),
    ('month', 'Months'),
    ('year', 'Years')
])
```

**Lợi ích:**
- Tự động tạo tasks định kỳ
- Maintenance tasks
- Regular reviews

---

### 1.2. Roadmap Nâng Cấp Module Công Việc

#### 🎯 Phase 1: Task Stages & Kanban (Tuần 1-2)

**Mục tiêu:** Implement workflow system như Odoo

**Tasks:**
1. ✅ **Create `cong_viec.trang_thai` Model** (Task Stage)
   ```python
   class CongViecTrangThai(models.Model):
       _name = 'cong_viec.trang_thai'
       _description = 'Trạng thái công việc'
       _order = 'sequence, id'
       
       name = fields.Char('Tên trạng thái', required=True)
       sequence = fields.Integer('Thứ tự', default=10)
       fold = fields.Boolean('Thu gọn trong Kanban')
       description = fields.Text('Mô tả')
       du_an_ids = fields.Many2many('du_an', string='Dự án')
       active = fields.Boolean(default=True)
   ```

2. ✅ **Update `cong_viec` Model**
   ```python
   # Thay đổi từ Selection → Many2one
   # OLD:
   trang_thai = fields.Selection([...])
   
   # NEW:
   trang_thai_id = fields.Many2one(
       'cong_viec.trang_thai',
       string='Trạng thái',
       group_expand='_read_group_stage_ids'
   )
   kanban_state = fields.Selection([
       ('normal', 'Xám - Đúng tiến độ'),
       ('done', 'Xanh - Sẵn sàng'),
       ('blocked', 'Đỏ - Bị chặn')
   ], default='normal')
   ```

3. ✅ **Create Default Stages**
   ```xml
   <!-- data/cong_viec_stage_data.xml -->
   <record id="stage_new" model="cong_viec.trang_thai">
       <field name="name">Mới</field>
       <field name="sequence">1</field>
   </record>
   <record id="stage_in_progress" model="cong_viec.trang_thai">
       <field name="name">Đang thực hiện</field>
       <field name="sequence">5</field>
   </record>
   <record id="stage_review" model="cong_viec.trang_thai">
       <field name="name">Đang review</field>
       <field name="sequence">10</field>
   </record>
   <record id="stage_done" model="cong_viec.trang_thai">
       <field name="name">Hoàn thành</field>
       <field name="sequence">15</field>
       <field name="fold" eval="True"/>
   </record>
   ```

4. ✅ **Enhanced Kanban View**
   ```xml
   <kanban default_group_by="trang_thai_id" 
           on_create="quick_create" 
           quick_create_view="cong_viec_quick_create_form">
       <field name="color"/>
       <field name="kanban_state"/>
       <field name="priority"/>
       <progressbar field="kanban_state" 
                    colors='{"done": "success", "blocked": "danger"}'/>
       <templates>
           <t t-name="kanban-box">
               <!-- Kanban card design -->
               <div class="oe_kanban_global_click">
                   <div class="o_kanban_record_top">
                       <div class="o_kanban_record_headings">
                           <strong><field name="ten_cong_viec"/></strong>
                       </div>
                       <div class="o_kanban_record_top_right">
                           <field name="priority" widget="priority"/>
                       </div>
                   </div>
                   <div class="o_kanban_record_body">
                       <field name="tag_ids" widget="many2many_tags"/>
                       <field name="nguoi_phu_trach_id" widget="many2one_avatar_user"/>
                   </div>
                   <div class="o_kanban_record_bottom">
                       <div class="oe_kanban_bottom_left">
                           <field name="activity_ids" widget="kanban_activity"/>
                       </div>
                       <div class="oe_kanban_bottom_right">
                           <field name="kanban_state" widget="state_selection"/>
                       </div>
                   </div>
               </div>
           </t>
       </templates>
   </kanban>
   ```

**Output:**
- ✅ Flexible workflow system
- ✅ Drag & drop Kanban
- ✅ Progress bar per stage
- ✅ Quick create

---

#### 🎯 Phase 2: Subtasks & Dependencies (Tuần 3-4)

**1. Subtasks Implementation**
```python
class CongViec(models.Model):
    _name = 'cong_viec'
    
    # Subtasks
    parent_id = fields.Many2one(
        'cong_viec',
        string='Công việc cha',
        index=True
    )
    child_ids = fields.One2many(
        'cong_viec',
        'parent_id',
        string='Công việc con'
    )
    subtask_count = fields.Integer(
        compute='_compute_subtask_count',
        string='Số công việc con'
    )
    
    # Auto-compute progress từ subtasks
    @api.depends('child_ids.tien_do')
    def _compute_progress_from_subtasks(self):
        for task in self:
            if task.child_ids:
                total_progress = sum(task.child_ids.mapped('tien_do'))
                task.tien_do = total_progress / len(task.child_ids)
```

**2. Dependencies**
```python
# Many2many self-relation
phu_thuoc_vao_ids = fields.Many2many(
    'cong_viec',
    'cong_viec_dependencies_rel',
    'cong_viec_id',
    'depends_on_id',
    string='Phụ thuộc vào các công việc',
    help='Các công việc phải hoàn thành trước khi bắt đầu công việc này'
)

cong_viec_phu_thuoc_ids = fields.Many2many(
    'cong_viec',
    'cong_viec_dependencies_rel',
    'depends_on_id',
    'cong_viec_id',
    string='Các công việc phụ thuộc',
    help='Các công việc sẽ bắt đầu sau khi công việc này hoàn thành'
)

# Constraint: Cannot depend on itself
@api.constrains('phu_thuoc_vao_ids')
def _check_dependency_cycle(self):
    if not self._check_recursion(visited=set()):
        raise ValidationError('Không thể tạo vòng lặp phụ thuộc!')
```

**3. Gantt View với Dependencies**
```xml
<gantt date_start="ngay_bat_dau"
       date_stop="ngay_ket_thuc"
       string="Gantt Công Việc"
       default_scale="week"
       decoration-danger="trang_thai_id == ref('stage_blocked')"
       decoration-success="trang_thai_id == ref('stage_done')">
    <field name="nguoi_phu_trach_id"/>
    <field name="du_an_id"/>
    <field name="tien_do"/>
    
    <!-- Dependencies lines -->
    <field name="phu_thuoc_vao_ids" widget="task_dependency"/>
</gantt>
```

---

#### 🎯 Phase 3: Time Tracking & Timesheet (Tuần 5-6)

**1. Timesheet Model**
```python
class CongViecTimesheet(models.Model):
    _name = 'cong_viec.timesheet'
    _description = 'Bảng chấm công theo công việc'
    _order = 'ngay desc'
    
    cong_viec_id = fields.Many2one(
        'cong_viec',
        string='Công việc',
        required=True,
        ondelete='cascade'
    )
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True,
        default=lambda self: self.env['nhan_vien'].search(
            [('user_id', '=', self.env.uid)], limit=1
        )
    )
    ngay = fields.Date(
        string='Ngày',
        required=True,
        default=fields.Date.today
    )
    gio_lam = fields.Float(
        string='Số giờ',
        required=True
    )
    mo_ta = fields.Html(string='Mô tả công việc đã làm')
    
    # Billing (if needed)
    don_gia = fields.Float('Đơn giá/giờ')
    thanh_tien = fields.Float(
        compute='_compute_thanh_tien',
        string='Thành tiền',
        store=True
    )
    
    @api.depends('gio_lam', 'don_gia')
    def _compute_thanh_tien(self):
        for record in self:
            record.thanh_tien = record.gio_lam * record.don_gia
```

**2. Update CongViec Model**
```python
timesheet_ids = fields.One2many(
    'cong_viec.timesheet',
    'cong_viec_id',
    string='Chấm công'
)

# Time tracking fields
gio_du_kien = fields.Float('Giờ dự kiến', help='Số giờ ước tính để hoàn thành')
gio_thuc_te = fields.Float(
    compute='_compute_gio_thuc_te',
    string='Giờ thực tế',
    store=True
)
gio_con_lai = fields.Float(
    compute='_compute_gio_con_lai',
    string='Giờ còn lại'
)
ty_le_hoan_thanh_gio = fields.Float(
    compute='_compute_ty_le_hoan_thanh_gio',
    string='% Hoàn thành (theo giờ)'
)

@api.depends('timesheet_ids.gio_lam')
def _compute_gio_thuc_te(self):
    for task in self:
        task.gio_thuc_te = sum(task.timesheet_ids.mapped('gio_lam'))

@api.depends('gio_du_kien', 'gio_thuc_te')
def _compute_gio_con_lai(self):
    for task in self:
        task.gio_con_lai = task.gio_du_kien - task.gio_thuc_te

@api.depends('gio_thuc_te', 'gio_du_kien')
def _compute_ty_le_hoan_thanh_gio(self):
    for task in self:
        if task.gio_du_kien:
            task.ty_le_hoan_thanh_gio = min(
                (task.gio_thuc_te / task.gio_du_kien) * 100,
                100
            )
        else:
            task.ty_le_hoan_thanh_gio = 0
```

**3. Timesheet Views**
```xml
<!-- Tree view trong task form -->
<page string="Chấm công" name="timesheet">
    <field name="timesheet_ids">
        <tree editable="bottom">
            <field name="ngay"/>
            <field name="nhan_vien_id"/>
            <field name="gio_lam" sum="Tổng giờ"/>
            <field name="mo_ta"/>
            <field name="don_gia" optional="hide"/>
            <field name="thanh_tien" sum="Tổng" optional="hide"/>
        </tree>
    </field>
    <group>
        <group>
            <field name="gio_du_kien"/>
            <field name="gio_thuc_te"/>
        </group>
        <group>
            <field name="gio_con_lai"/>
            <field name="ty_le_hoan_thanh_gio" widget="progressbar"/>
        </group>
    </group>
</page>
```

---

#### 🎯 Phase 4: Advanced Features (Tuần 7-8)

**1. Recurring Tasks**
```python
class CongViecLapLai(models.Model):
    _name = 'cong_viec.lap_lai'
    _description = 'Công việc lặp lại'
    
    cong_viec_id = fields.Many2one('cong_viec', required=True)
    lap_lai = fields.Boolean('Lặp lại', default=True)
    kieu_lap_lai = fields.Selection([
        ('hang_ngay', 'Hàng ngày'),
        ('hang_tuan', 'Hàng tuần'),
        ('hang_thang', 'Hàng tháng'),
        ('hang_quy', 'Hàng quý'),
        ('hang_nam', 'Hàng năm')
    ], string='Kiểu lặp lại')
    
    chu_ky = fields.Integer('Chu kỳ', default=1)
    ngay_bat_dau = fields.Date('Ngày bắt đầu')
    ngay_ket_thuc = fields.Date('Ngày kết thúc')
    
    # Cron job sẽ chạy method này
    @api.model
    def _create_recurring_tasks(self):
        """Tự động tạo tasks định kỳ"""
        today = fields.Date.today()
        recurring_configs = self.search([
            ('lap_lai', '=', True),
            '|',
            ('ngay_ket_thuc', '=', False),
            ('ngay_ket_thuc', '>=', today)
        ])
        
        for config in recurring_configs:
            # Logic tạo task mới dựa trên config
            pass
```

**2. Priority System**
```python
# Trong cong_viec model
priority = fields.Selection([
    ('0', 'Thấp'),
    ('1', 'Trung bình'),
    ('2', 'Cao'),
    ('3', 'Khẩn cấp')
], default='1', index=True)

# Auto-compute priority dựa trên deadline
@api.depends('ngay_ket_thuc')
def _compute_auto_priority(self):
    for task in self:
        if task.ngay_ket_thuc:
            days_left = (task.ngay_ket_thuc - fields.Date.today()).days
            if days_left < 0:
                task.priority = '3'  # Overdue = Urgent
            elif days_left <= 3:
                task.priority = '2'  # High
            elif days_left <= 7:
                task.priority = '1'  # Medium
            else:
                task.priority = '0'  # Low
```

**3. Rating & Feedback**
```python
class CongViecDanhGia(models.Model):
    _name = 'cong_viec.danh_gia'
    _description = 'Đánh giá công việc'
    
    cong_viec_id = fields.Many2one('cong_viec', required=True, ondelete='cascade')
    nguoi_danh_gia_id = fields.Many2one('nhan_vien', 'Người đánh giá')
    diem = fields.Selection([
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐')
    ], string='Điểm')
    nhan_xet = fields.Text('Nhận xét')
    ngay_danh_gia = fields.Datetime(default=fields.Datetime.now)
```

---

### 1.3. Dashboard & Analytics

**Task Analytics View**
```xml
<!-- Pivot view -->
<pivot string="Phân tích công việc">
    <field name="du_an_id" type="row"/>
    <field name="trang_thai_id" type="col"/>
    <field name="nguoi_phu_trach_id" type="row"/>
    <field name="gio_thuc_te" type="measure"/>
    <field name="gio_du_kien" type="measure"/>
</pivot>

<!-- Graph view -->
<graph string="Biểu đồ công việc" type="bar" stacked="True">
    <field name="trang_thai_id"/>
    <field name="nguoi_phu_trach_id" interval="week"/>
</graph>
```

---

## 🔍 PART 2: PHÂN TÍCH MODULE NHÂN SỰ

### 2.1. So Sánh Với Odoo HR Module

#### Cấu Trúc Hiện Tại (`nhan_su`)

**Models:**
- `nhan_vien` - Nhân viên
- `phong_ban` - Phòng ban
- `chuc_vu` - Chức vụ
- `lich_su_lam_viec` - Lịch sử
- `nhan_vien.ky_nang` - Kỹ năng
- `nhan_vien.chung_chi` - Chứng chỉ
- `nhan_vien.nguoi_phu_thuoc` - Người phụ thuộc
- `nhan_vien.hop_dong` - Hợp đồng

**Điểm Mạnh:**
✅ Có đầy đủ thông tin cơ bản  
✅ Có quản lý hợp đồng  
✅ Có kỹ năng & chứng chỉ  
✅ Có người phụ thuộc  
✅ Có tracking lương & phụ cấp  

**Điểm Yếu:**
❌ Không có Attendance tracking  
❌ Thiếu Leave management  
❌ Không có Performance appraisal  
❌ Thiếu Recruitment process  
❌ Không có Expense management  
❌ Thiếu Skills matrix & gap analysis  
❌ Không có Employee directory với ảnh  

---

#### Odoo HR Module - Tính Năng Nổi Bật

**1. hr.employee Model Structure**
```python
class Employee(models.Model):
    _name = "hr.employee"
    _inherit = ['mail.thread', 'mail.activity.mixin', 
                'resource.mixin', 'avatar.mixin']
    
    # Resource mixin provides calendar & working hours
    resource_id = fields.Many2one('resource.resource')
    resource_calendar_id = fields.Many2one('resource.calendar')
    
    # Manager hierarchy
    parent_id = fields.Many2one('hr.employee', 'Manager')
    coach_id = fields.Many2one('hr.employee', 'Coach')
    child_ids = fields.One2many('hr.employee', 'parent_id')
    
    # Work information
    job_id = fields.Many2one('hr.job', 'Job Position')
    department_id = fields.Many2one('hr.department')
    company_id = fields.Many2one('res.company')
    
    # Contract & Salary (from hr_contract module)
    contract_ids = fields.One2many('hr.contract', 'employee_id')
    
    # Badge & Check-in (from hr_attendance)
    attendance_ids = fields.One2many('hr.attendance', 'employee_id')
    last_attendance_id = fields.Many2one('hr.attendance')
    
    # Skills (from hr_skills module)
    employee_skill_ids = fields.One2many('hr.employee.skill', 'employee_id')
```

---

**2. hr.department - Phòng Ban**
```python
class Department(models.Model):
    _name = "hr.department"
    
    name = fields.Char(required=True)
    complete_name = fields.Char(compute='_compute_complete_name', 
                                 recursive=True, store=True)
    parent_id = fields.Many2one('hr.department', 'Parent Department')
    child_ids = fields.One2many('hr.department', 'parent_id')
    manager_id = fields.Many2one('hr.employee', 'Manager')
    
    # Members
    member_ids = fields.One2many('hr.employee', 'department_id')
    total_employee = fields.Integer(compute='_compute_total_employee')
    
    # Jobs
    jobs_ids = fields.One2many('hr.job', 'department_id')
    
    # Colors & Organization
    color = fields.Integer()
    note = fields.Text()
```

---

**3. hr.job - Vị Trí Công Việc**
```python
class Job(models.Model):
    _name = "hr.job"
    
    name = fields.Char(required=True)
    department_id = fields.Many2one('hr.department')
    company_id = fields.Many2one('res.company')
    
    # Requirements
    requirements = fields.Text()
    description = fields.Html()
    
    # Statistics
    no_of_employee = fields.Integer(compute='_compute_employees')
    no_of_recruitment = fields.Integer('Expected New Employees')
    no_of_hired_employee = fields.Integer('Hired Employees')
    
    # State
    state = fields.Selection([
        ('recruit', 'Recruitment in Progress'),
        ('open', 'Not Recruiting')
    ], default='open')
```

---

### 2.2. Roadmap Nâng Cấp Module Nhân Sự

#### 🎯 Phase 1: Enhanced Employee Profile (Tuần 1-2)

**1. Avatar & Photos**
```python
class NhanVien(models.Model):
    _inherit = ['avatar.mixin']  # Add avatar mixin
    
    # Replace anh_dai_dien with avatar field
    image_1920 = fields.Image(max_width=1920, max_height=1920)
    image_1024 = fields.Image(related='image_1920', max_width=1024, max_height=1024)
    image_512 = fields.Image(related='image_1920', max_width=512, max_height=512)
    image_256 = fields.Image(related='image_1920', max_width=256, max_height=256)
    image_128 = fields.Image(related='image_1920', max_width=128, max_height=128)
    
    # Avatar for kanban/list views
    avatar_1920 = fields.Image(compute='_compute_avatar_1920')
    avatar_1024 = fields.Image(compute='_compute_avatar_1024')
    avatar_512 = fields.Image(compute='_compute_avatar_512')
    avatar_256 = fields.Image(compute='_compute_avatar_256')
    avatar_128 = fields.Image(compute='_compute_avatar_128')
```

**2. Work Location & Calendar**
```python
# Integration với resource.mixin
_inherit = ['resource.mixin']

resource_id = fields.Many2one('resource.resource', ondelete='cascade')
resource_calendar_id = fields.Many2one(
    'resource.calendar',
    string='Lịch làm việc',
    default=lambda self: self.env.company.resource_calendar_id
)

# Timezone
tz = fields.Selection(
    string='Timezone',
    related='resource_id.tz',
    readonly=False
)
```

**3. Work Address**
```python
work_location_id = fields.Many2one('hr.work.location', 'Địa điểm làm việc')

# Or simple text fields
work_address = fields.Text('Địa chỉ làm việc')
work_phone = fields.Char('Số điện thoại công việc')
work_email = fields.Char('Email công việc')
```

---

#### 🎯 Phase 2: Attendance Management (Tuần 3-4)

**1. Attendance Model**
```python
class NhanVienChamCong(models.Model):
    _name = 'nhan_vien.cham_cong'
    _description = 'Chấm công'
    _order = 'check_in desc'
    
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        required=True,
        ondelete='cascade'
    )
    check_in = fields.Datetime('Check In', required=True)
    check_out = fields.Datetime('Check Out')
    
    worked_hours = fields.Float(
        compute='_compute_worked_hours',
        string='Giờ làm việc',
        store=True
    )
    
    # Location (if using mobile check-in)
    check_in_latitude = fields.Float()
    check_in_longitude = fields.Float()
    check_out_latitude = fields.Float()
    check_out_longitude = fields.Float()
    
    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for att in self:
            if att.check_out:
                delta = att.check_out - att.check_in
                att.worked_hours = delta.total_seconds() / 3600
            else:
                att.worked_hours = 0
    
    @api.constrains('check_in', 'check_out')
    def _check_validity(self):
        for att in self:
            if att.check_out and att.check_out < att.check_in:
                raise ValidationError('Check out phải sau check in!')
```

**2. Update NhanVien Model**
```python
cham_cong_ids = fields.One2many('nhan_vien.cham_cong', 'nhan_vien_id')
last_cham_cong_id = fields.Many2one(
    'nhan_vien.cham_cong',
    compute='_compute_last_attendance'
)
attendance_state = fields.Selection([
    ('checked_out', 'Đã check out'),
    ('checked_in', 'Đã check in')
], compute='_compute_attendance_state')

hours_last_month = fields.Float(compute='_compute_hours_last_month')
hours_today = fields.Float(compute='_compute_hours_today')
```

**3. Kiosk Mode View**
```xml
<!-- Màn hình check-in/out tại công ty -->
<form string="Chấm công" create="false">
    <sheet>
        <div class="text-center">
            <field name="nhan_vien_id" 
                   widget="many2one_avatar_employee"
                   options="{'no_create': True, 'no_open': True}"/>
            
            <h1 class="mt-3">
                <field name="ho_ten" readonly="1"/>
            </h1>
            
            <div class="mt-4">
                <button name="action_check_in" 
                        string="CHECK IN"
                        type="object"
                        class="btn-success btn-lg"
                        attrs="{'invisible': [('attendance_state', '=', 'checked_in')]}"/>
                        
                <button name="action_check_out"
                        string="CHECK OUT"
                        type="object"
                        class="btn-danger btn-lg"
                        attrs="{'invisible': [('attendance_state', '=', 'checked_out')]}"/>
            </div>
            
            <div class="mt-3">
                <field name="hours_today"/> giờ hôm nay
            </div>
        </div>
    </sheet>
</form>
```

---

#### 🎯 Phase 3: Leave Management (Tuần 5-6)

**1. Leave Type**
```python
class LoaiNghiPhep(models.Model):
    _name = 'nhan_vien.loai_nghi_phep'
    _description = 'Loại nghỉ phép'
    
    name = fields.Char('Tên', required=True)
    code = fields.Char('Mã')
    
    # Allocation
    allocation_type = fields.Selection([
        ('no', 'Không phân bổ'),
        ('fixed', 'Cố định'),
        ('fixed_allocation', 'Phân bổ cố định hàng năm')
    ], default='fixed')
    
    so_ngay_mac_dinh = fields.Float('Số ngày mặc định/năm')
    
    # Validation
    can_phe_duyet = fields.Boolean('Cần phê duyệt', default=True)
    max_ngay_lien_tiep = fields.Integer('Số ngày tối đa liên tiếp')
    
    # Color
    color = fields.Integer()
```

**2. Leave Allocation**
```python
class NghiPhepPhanBo(models.Model):
    _name = 'nhan_vien.nghi_phep.phan_bo'
    _description = 'Phân bổ nghỉ phép'
    
    nhan_vien_id = fields.Many2one('nhan_vien', required=True)
    loai_nghi_phep_id = fields.Many2one('nhan_vien.loai_nghi_phep', required=True)
    
    so_ngay_duoc_phep = fields.Float('Số ngày được phép')
    so_ngay_da_nghi = fields.Float(compute='_compute_leaves')
    so_ngay_con_lai = fields.Float(compute='_compute_leaves')
    
    nam = fields.Integer('Năm', default=lambda self: fields.Date.today().year)
    
    @api.depends('nhan_vien_id', 'loai_nghi_phep_id', 'nam')
    def _compute_leaves(self):
        # Calculate from actual leave requests
        pass
```

**3. Leave Request**
```python
class NghiPhep(models.Model):
    _name = 'nhan_vien.nghi_phep'
    _description = 'Đơn xin nghỉ phép'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    nhan_vien_id = fields.Many2one('nhan_vien', required=True)
    loai_nghi_phep_id = fields.Many2one('nhan_vien.loai_nghi_phep', required=True)
    
    ngay_bat_dau = fields.Date('Từ ngày', required=True)
    ngay_ket_thuc = fields.Date('Đến ngày', required=True)
    so_ngay = fields.Float(compute='_compute_so_ngay', store=True)
    
    ly_do = fields.Text('Lý do')
    
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('confirm', 'Chờ duyệt'),
        ('approve', 'Đã duyệt'),
        ('refuse', 'Từ chối'),
        ('cancel', 'Hủy')
    ], default='draft', tracking=True)
    
    nguoi_duyet_id = fields.Many2one('nhan_vien', 'Người duyệt')
    ngay_duyet = fields.Datetime('Ngày duyệt')
    
    # Actions
    def action_confirm(self):
        self.write({'trang_thai': 'confirm'})
        # Send notification to manager
        
    def action_approve(self):
        self.write({
            'trang_thai': 'approve',
            'nguoi_duyet_id': self.env.user.nhan_vien_id.id,
            'ngay_duyet': fields.Datetime.now()
        })
        
    def action_refuse(self):
        self.write({'trang_thai': 'refuse'})
```

---

#### 🎯 Phase 4: Skills & Recruitment (Tuần 7-8)

**1. Skills Management**
```python
class KyNang(models.Model):
    _name = 'nhan_vien.ky_nang'
    # Enhance existing model
    
    loai_ky_nang = fields.Selection([
        ('technical', 'Kỹ năng kỹ thuật'),
        ('soft', 'Kỹ năng mềm'),
        ('language', 'Ngôn ngữ'),
        ('certification', 'Chứng chỉ')
    ])
    
class NhanVienKyNangRel(models.Model):
    """Many2many relation với levels"""
    _name = 'nhan_vien.ky_nang.rel'
    _description = 'Kỹ năng của nhân viên'
    
    nhan_vien_id = fields.Many2one('nhan_vien', required=True)
    ky_nang_id = fields.Many2one('nhan_vien.ky_nang', required=True)
    
    trinh_do = fields.Selection([
        ('1', 'Cơ bản'),
        ('2', 'Trung bình'),
        ('3', 'Khá'),
        ('4', 'Giỏi'),
        ('5', 'Chuyên gia')
    ], required=True)
    
    nam_kinh_nghiem = fields.Integer('Số năm kinh nghiệm')
    chung_chi = fields.Char('Chứng chỉ liên quan')
```

**2. Recruitment**
```python
class TuyenDung(models.Model):
    _name = 'nhan_vien.tuyen_dung'
    _description = 'Tuyển dụng'
    _inherit = ['mail.thread']
    
    vi_tri_id = fields.Many2one('chuc_vu', 'Vị trí tuyển dụng')
    phong_ban_id = fields.Many2one('phong_ban')
    
    mo_ta_cong_viec = fields.Html('Mô tả công việc')
    yeu_cau = fields.Html('Yêu cầu')
    quyen_loi = fields.Html('Quyền lợi')
    
    so_luong = fields.Integer('Số lượng cần tuyển')
    han_nop = fields.Date('Hạn nộp hồ sơ')
    
    # Applications
    ung_vien_ids = fields.One2many('nhan_vien.ung_vien', 'tuyen_dung_id')
    
class UngVien(models.Model):
    _name = 'nhan_vien.ung_vien'
    _description = 'Ứng viên'
    
    tuyen_dung_id = fields.Many2one('nhan_vien.tuyen_dung')
    
    ho_ten = fields.Char(required=True)
    email = fields.Char()
    dien_thoai = fields.Char()
    
    cv_file = fields.Binary('CV')
    cv_filename = fields.Char()
    
    trang_thai = fields.Selection([
        ('new', 'Mới'),
        ('screening', 'Sàng lọc'),
        ('interview', 'Phỏng vấn'),
        ('offer', 'Đề nghị'),
        ('hired', 'Đã tuyển'),
        ('refused', 'Từ chối')
    ], default='new')
```

---

### 2.3. Dashboard & Reports

**HR Dashboard**
```python
# Dashboard actions
def action_open_dashboard(self):
    return {
        'type': 'ir.actions.client',
        'tag': 'hr_dashboard',
        'name': 'HR Dashboard'
    }
```

**Reports:**
1. Employee headcount by department
2. Attendance report
3. Leave balance report
4. Skills matrix
5. Recruitment funnel

---

## 📋 SUMMARY & NEXT STEPS

### Ưu Tiên Triển Khai

**HIGH PRIORITY (Làm trước):**
1. ✅ Task Stages & Kanban (quan_ly_cong_viec)
2. ✅ Enhanced Employee Profile (nhan_su)
3. ✅ Attendance Management (nhan_su)
4. ✅ Subtasks (quan_ly_cong_viec)

**MEDIUM PRIORITY:**
5. Time Tracking & Timesheet
6. Leave Management
7. Dependencies & Gantt
8. Skills & Recruitment

**LOW PRIORITY (Tính năng nâng cao):**
9. Recurring tasks
10. Performance appraisal
11. Expense management
12. Advanced analytics

---

## 🚀 Implementation Timeline

| Tuần | Module | Feature | Status |
|------|--------|---------|--------|
| 1-2 | quan_ly_cong_viec | Task Stages & Kanban | 🔄 Ready |
| 3-4 | quan_ly_cong_viec | Subtasks & Dependencies | 📋 Planned |
| 5-6 | quan_ly_cong_viec | Time Tracking | 📋 Planned |
| 1-2 | nhan_su | Enhanced Profile & Avatar | 🔄 Ready |
| 3-4 | nhan_su | Attendance Management | 📋 Planned |
| 5-6 | nhan_su | Leave Management | 📋 Planned |
| 7-8 | Both | Advanced Features | 📋 Planned |

---

**Prepared by:** AI Assistant  
**Date:** 2026-01-28  
**Next Action:** Bắt đầu Phase 1 - Task Stages & Kanban cho module quan_ly_cong_viec
