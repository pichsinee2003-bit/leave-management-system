from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ระบบบริหารจัดการการลางาน (Leave Management System)</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    <!-- Google Fonts (Sarabun) -->
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        body {
            font-family: 'Sarabun', sans-serif;
            background-color: #f4f6f9;
            color: #333;
            min-height: 100vh;
        }
        .login-container {
            max-width: 450px;
            width: 100%;
        }
        .card {
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        }
        .card-header {
            background-color: #1e293b;
            color: #ffffff;
            border-top-left-radius: 12px !important;
            border-top-right-radius: 12px !important;
            font-weight: 600;
        }
        .nav-pills .nav-link.active {
            background-color: #2563eb;
        }
        .status-badge {
            font-size: 0.85rem;
            padding: 6px 12px;
            border-radius: 20px;
        }
        /* Calendar Styling */
        .calendar-table th {
            text-align: center;
            background-color: #f8fafc;
            width: 14.28%;
        }
        .calendar-cell {
            height: 115px;
            vertical-align: top;
            background-color: #ffffff;
            font-size: 0.82rem;
        }
        .calendar-cell.other-month {
            background-color: #f9fafb;
            color: #9ca3af;
        }
        .calendar-cell.today {
            background-color: #eff6ff;
            border: 2px solid #2563eb !important;
        }
        .leave-event-badge {
            font-size: 0.68rem;
            padding: 2px 4px;
            border-radius: 4px;
            margin-bottom: 2px;
            display: block;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: left;
        }
        .holiday-badge {
            font-size: 0.68rem;
            padding: 2px 4px;
            border-radius: 4px;
            margin-bottom: 2px;
            display: block;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: left;
            background-color: #dc3545;
            color: white;
        }
    </style>
</head>
<body>

    <!-- ==================== 1. PAGE: LOGIN VIEW ==================== -->
    <div id="loginView" class="d-flex align-items-center justify-content-center min-vh-100 py-4">
        <div class="login-container px-3">
            <div class="text-center mb-4">
                <i class="bi bi-building-gear text-primary display-3"></i>
                <h3 class="fw-bold mt-2">ระบบบริหารจัดการการลางาน</h3>
                <p class="text-muted small">กรุณาเข้าสู่ระบบเพื่อใช้งาน (รองรับผู้อนุมัติหลายคนต่อบริษัท)</p>
            </div>

            <div class="card p-3">
                <ul class="nav nav-pills nav-justified mb-3" id="loginTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active fw-bold" id="emp-tab" data-bs-toggle="tab" data-bs-target="#empLoginTab" type="button">
                            <i class="bi bi-person me-1"></i> พนักงาน
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link fw-bold" id="appr-tab" data-bs-toggle="tab" data-bs-target="#apprLoginTab" type="button">
                            <i class="bi bi-shield-lock me-1"></i> ผู้อนุมัติ / HR
                        </button>
                    </li>
                </ul>

                <div class="tab-content p-2" id="loginTabContent">
                    <!-- Employee Login Form -->
                    <div class="tab-pane fade show active" id="empLoginTab">
                        <form onsubmit="handleEmployeeLogin(event)">
                            <div class="mb-3">
                                <label class="form-label fw-bold small"><i class="bi bi-building me-1"></i> เลือกบริษัท:</label>
                                <select id="loginCompanySelect" class="form-select" onchange="onLoginCompanyChange(this.value)">
                                    <!-- Dynamic -->
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold small"><i class="bi bi-person-circle me-1"></i> เลือกพนักงาน:</label>
                                <select id="loginUserSelect" class="form-select">
                                    <!-- Dynamic -->
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold small"><i class="bi bi-key me-1"></i> รหัสผ่านเข้าใช้งาน:</label>
                                <input type="password" id="empPassword" class="form-control" placeholder="กรอกรหัสผ่าน (ทดสอบ: 1234)" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">
                                <i class="bi bi-box-arrow-in-right me-1"></i> เข้าสู่ระบบพนักงาน
                            </button>
                        </form>
                    </div>

                    <!-- Approver / HR Admin Login Form -->
                    <div class="tab-pane fade" id="apprLoginTab">
                        <form onsubmit="handleApproverLogin(event)">
                            <div class="mb-3 d-flex justify-content-between align-items-center">
                                <label class="form-label fw-bold small mb-0"><i class="bi bi-building me-1"></i> เลือกบริษัท:</label>
                                <button type="button" class="btn btn-outline-primary btn-sm py-0 px-2 fw-bold" style="font-size: 0.75rem;" onclick="openAddCompanyModal()">
                                    <i class="bi bi-plus-circle me-1"></i> + เพิ่มบริษัทใหม่
                                </button>
                            </div>
                            <div class="mb-3 mt-1">
                                <select id="loginApprCompanySelect" class="form-select" onchange="onLoginApprCompanyChange(this.value)">
                                    <!-- Dynamic -->
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold small"><i class="bi bi-person-badge me-1"></i> เลือกผู้อนุมัติ:</label>
                                <select id="loginApprUserSelect" class="form-select">
                                    <!-- Dynamic -->
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold small"><i class="bi bi-key me-1"></i> รหัสผ่าน (Password):</label>
                                <input type="password" id="apprPassword" class="form-control" placeholder="กรอกรหัสผ่าน (ทดสอบ: 1234)" required>
                            </div>
                            <button type="submit" class="btn btn-warning w-100 py-2 fw-bold text-dark">
                                <i class="bi bi-shield-check me-1"></i> เข้าสู่ระบบผู้อนุมัติ / HR
                            </button>
                        </form>
                    </div>
                </div>

                <div class="alert alert-secondary mt-3 mb-0 p-2 text-center small">
                    <i class="bi bi-info-circle me-1"></i> รหัสผ่านทดสอบเริ่มต้นคือ: <strong>1234</strong>
                </div>
            </div>
        </div>
    </div>


    <!-- ==================== 2. PAGE: MAIN SYSTEM VIEW ==================== -->
    <div id="appView" class="d-none">
        
        <!-- Navigation Bar -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark py-3">
            <div class="container">
                <a class="navbar-brand d-flex align-items-center" href="#">
                    <i class="bi bi-building-gear me-2 fs-3 text-primary"></i>
                    <span>ระบบบริหารจัดการการลางาน</span>
                </a>
                
                <div class="d-flex align-items-center gap-3">
                    <div class="text-light text-end me-2">
                        <div id="navUserName" class="fw-bold small">-</div>
                        <div id="navUserRole" class="text-muted" style="font-size: 0.75rem;">-</div>
                    </div>
                    <button class="btn btn-outline-danger btn-sm rounded-pill px-3" onclick="handleLogout()">
                        <i class="bi bi-box-arrow-right me-1"></i> ออกจากระบบ
                    </button>
                </div>
            </div>
        </nav>

        <div class="container my-4">

            <!-- SECTION: EMPLOYEE VIEW -->
            <div id="employeeSection" class="d-none">
                <!-- Quota Bar -->
                <div class="card p-3 mb-4">
                    <div class="row align-items-center">
                        <div class="col-md-4 border-end">
                            <h6 class="fw-bold text-primary mb-1" id="empInfoCompany">-</h6>
                            <h5 class="fw-bold mb-0" id="empInfoName">-</h5>
                            <small class="text-muted" id="empInfoDept">-</small>
                        </div>
                        <div class="col-md-8">
                            <div id="empQuotaDisplayGrid" class="d-flex flex-wrap justify-content-around text-center gap-2">
                                <!-- Dynamic Quotas Rendered Here -->
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <!-- Leave Request Form -->
                    <div class="col-lg-5 mb-4">
                        <div class="card">
                            <div class="card-header py-3">
                                <i class="bi bi-file-earmark-plus me-2"></i> ยื่นคำขอลางาน
                            </div>
                            <div class="card-body p-4">
                                <form id="leaveForm" onsubmit="handleLeaveSubmit(event)">
                                    <div class="mb-3">
                                        <label class="form-label fw-bold">ประเภทการลา <span class="text-danger">*</span></label>
                                        <select id="leaveType" class="form-select" onchange="toggleReasonField()" required>
                                            <option value="">-- กรุณาเลือกประเภทการลา --</option>
                                        </select>
                                    </div>

                                    <div class="mb-3">
                                        <label class="form-label fw-bold">รูปแบบการลา <span class="text-danger">*</span></label>
                                        <div class="d-flex gap-3 bg-light p-2 rounded border">
                                            <div class="form-check">
                                                <input class="form-check-input" type="radio" name="durationMode" id="modeFull" value="full" checked onchange="onDurationModeChange()">
                                                <label class="form-check-label fw-semibold" for="modeFull">
                                                    เต็มวัน (Full Day)
                                                </label>
                                            </div>
                                            <div class="form-check">
                                                <input class="form-check-input" type="radio" name="durationMode" id="modeHalf" value="half" onchange="onDurationModeChange()">
                                                <label class="form-check-label fw-semibold text-primary" for="modeHalf">
                                                    <i class="bi bi-clock me-1"></i> ครึ่งวัน (0.5 วัน)
                                                </label>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="mb-3 d-none" id="halfDaySessionContainer">
                                        <label class="form-label fw-bold text-primary">ช่วงเวลาการลาครึ่งวัน <span class="text-danger">*</span></label>
                                        <select id="halfDaySession" class="form-select border-primary" onchange="calculateDays()">
                                            <option value="morning">รอบเช้า (08:30 - 12:30)</option>
                                            <option value="afternoon">รอบบ่าย (13:30 - 17:30)</option>
                                        </select>
                                    </div>

                                    <div class="mb-3" id="reasonContainer">
                                        <label class="form-label fw-bold">เหตุผลการลา <span class="text-danger">*</span></label>
                                        <textarea id="leaveReason" class="form-control" rows="2" placeholder="ระบุรายละเอียด/เหตุผลการลางาน..." required></textarea>
                                    </div>

                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label fw-bold" id="startDateLabel">วันที่เริ่มต้น <span class="text-danger">*</span></label>
                                            <input type="date" id="startDate" class="form-control" onchange="calculateDays()" required>
                                        </div>
                                        <div class="col-md-6 mb-3" id="endDateColContainer">
                                            <label class="form-label fw-bold">วันที่สิ้นสุด <span class="text-danger">*</span></label>
                                            <input type="date" id="endDate" class="form-control" onchange="calculateDays()" required>
                                        </div>
                                    </div>

                                    <!-- HANDOVER / DELEGATION OF AUTHORITY SECTION -->
                                    <div class="card bg-light p-3 mb-3 border">
                                        <h6 class="fw-bold text-dark mb-2"><i class="bi bi-people-fill text-primary me-1"></i> มอบหมายงานแทนระหว่างลา (Task Handover)</h6>
                                        <div class="mb-2">
                                            <label class="form-label small fw-bold">ผู้ปฏิบัติงานแทน:</label>
                                            <select id="handoverColleague" class="form-select form-select-sm">
                                                <option value="-">-- เลือกเพื่อนร่วมงานปฏิบัติงานแทน (ไม่ระบุได้) --</option>
                                            </select>
                                        </div>
                                        <div>
                                            <label class="form-label small fw-bold">รายการงานค้าง / โน้ตส่งมอบงาน / ลิงก์เอกสาร:</label>
                                            <textarea id="handoverNotes" class="form-control form-control-sm" rows="2" placeholder="เช่น ฝากดูแลเคสลูกค้า A, ตรวจสอบระบบเบื้องต้น, ลิงก์เอกสารงาน..."></textarea>
                                        </div>
                                    </div>

                                    <div class="mb-3 p-3 bg-light rounded border text-center">
                                        <div class="fw-bold text-secondary">จำนวนวันลาครั้งนี้:</div>
                                        <span id="calculatedDaysText" class="fw-bold fs-4 text-primary">0 วัน</span>
                                        <div class="text-muted small mt-1"><i class="bi bi-info-circle me-1"></i>ระบบหักวันหยุดนักขัตฤกษ์และวันอาทิตย์ให้อัตโนมัติ</div>
                                    </div>

                                    <div class="mb-3">
                                        <label class="form-label fw-bold">แนบไฟล์เอกสาร (รูปภาพ, PDF)</label>
                                        <input type="file" id="leaveFile" class="form-control" accept="image/*,.pdf">
                                    </div>

                                    <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">
                                        <i class="bi bi-send me-1"></i> ส่งคำขอลางาน
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>

                    <!-- Employee Leave History -->
                    <div class="col-lg-7">
                        <div class="card">
                            <div class="card-header py-3 d-flex justify-content-between align-items-center">
                                <span><i class="bi bi-clock-history me-2"></i> ประวัติและสถานะการลางานของฉัน</span>
                                <small class="text-white-50"><i class="bi bi-info-circle me-1"></i> ขอยกเลิกได้ทั้งตอนรออนุมัติหรือหลังอนุมัติ</small>
                            </div>
                            <div class="card-body p-0">
                                <div class="table-responsive">
                                    <table class="table table-hover align-middle mb-0">
                                        <thead class="table-light">
                                            <tr>
                                                <th>วันที่ยื่น</th>
                                                <th>ประเภท</th>
                                                <th>ช่วงวันที่ลา</th>
                                                <th>ผู้ปฏิบัติงานแทน</th>
                                                <th>สถานะ</th>
                                                <th class="text-center">จัดการ</th>
                                            </tr>
                                        </thead>
                                        <tbody id="employeeHistoryTable">
                                            <!-- Data rendered dynamically -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SECTION: APPROVER / HR ADMIN VIEW -->
            <div id="approverSection" class="d-none">
                <div class="alert alert-info d-flex align-items-center justify-content-between shadow-sm mb-4 flex-wrap gap-2">
                    <div class="d-flex align-items-center gap-3">
                        <i class="bi bi-shield-check fs-3"></i>
                        <div>
                            <strong>โหมดผู้บริหาร / ผู้อนุมัติ:</strong> ท่านกำลังจัดการระบบของ
                            <span id="approverCompanyText" class="badge bg-primary fs-6 ms-1">-</span>
                        </div>
                    </div>
                    <div class="d-flex gap-2 flex-wrap">
                        <button class="btn btn-success btn-sm fw-bold" onclick="openAddApproverModal()">
                            <i class="bi bi-shield-plus me-1"></i> + เพิ่มผู้อนุมัติใหม่
                        </button>
                        <button class="btn btn-primary btn-sm fw-bold" onclick="openAddEmployeeModal()">
                            <i class="bi bi-person-plus-fill me-1"></i> เพิ่มพนักงานใหม่
                        </button>
                        <button class="btn btn-info btn-sm fw-bold text-dark" onclick="openHolidayModal()">
                            <i class="bi bi-calendar-event me-1"></i> วันหยุด
                        </button>
                        <button class="btn btn-dark btn-sm fw-bold" onclick="openLeaveTypeConfigModal()">
                            <i class="bi bi-gear-fill me-1"></i> ประเภทการลา
                        </button>
                        <button class="btn btn-warning btn-sm fw-bold text-dark" onclick="openResetModal()">
                            <i class="bi bi-arrow-counterclockwise me-1"></i> รีเซ็ต
                        </button>
                    </div>
                </div>

                <!-- NOTIFICATION ALERT BANNER FOR APPROVER -->
                <div id="approverNotificationBanner" class="alert alert-danger shadow-sm mb-4 d-none align-items-center justify-content-between">
                    <div class="d-flex align-items-center gap-2">
                        <i class="bi bi-bell-fill fs-4"></i>
                        <div>
                            <strong>🔔 แจ้งเตือนรายการใหม่:</strong> มีรายการที่ต้องตรวจสอบจำนวน <span id="pendingNotificationCount" class="badge bg-white text-danger fw-bold fs-6">0</span> รายการ (คำขอลาใหม่ / คำขอคืนวันลา)
                        </div>
                    </div>
                    <button class="btn btn-sm btn-light text-danger fw-bold shadow-sm" onclick="scrollToPendingTable()">
                        ตรวจสอบทันที
                    </button>
                </div>

                <!-- TEAM LEAVE CALENDAR VIEW -->
                <div class="card mb-4">
                    <div class="card-header bg-primary py-3 d-flex justify-content-between align-items-center flex-wrap gap-2">
                        <span><i class="bi bi-calendar-check-fill me-2"></i> ปฏิทินวันลาและวันหยุดนักขัตฤกษ์ของทีม</span>
                        <div class="d-flex align-items-center gap-2">
                            <button class="btn btn-sm btn-light fw-bold" onclick="changeCalendarMonth(-1)"><i class="bi bi-chevron-left"></i> เดือนก่อนหน้า</button>
                            <span id="currentCalendarMonthLabel" class="text-white fw-bold px-2" style="font-size: 1.05rem;">-</span>
                            <button class="btn btn-sm btn-light fw-bold" onclick="changeCalendarMonth(1)">เดือนถัดไป <i class="bi bi-chevron-right"></i></button>
                        </div>
                    </div>
                    <div class="card-body p-3">
                        <div class="table-responsive">
                            <table class="table table-bordered calendar-table mb-0">
                                <thead>
                                    <tr>
                                        <th class="text-danger">อาทิตย์</th>
                                        <th>จันทร์</th>
                                        <th>อังคาร</th>
                                        <th>พุธ</th>
                                        <th>พฤหัสบดี</th>
                                        <th>ศุกร์</th>
                                        <th class="text-primary">เสาร์</th>
                                    </tr>
                                </thead>
                                <tbody id="teamCalendarBody">
                                    <!-- Dynamic Calendar Grid -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- HR Quota Management Table -->
                <div class="card mb-4">
                    <div class="card-header bg-dark py-3 d-flex justify-content-between align-items-center">
                        <span><i class="bi bi-people-fill me-2"></i> จัดการบัญชีพนักงานและโควตาวันลา (User Management & Quotas)</span>
                        <span class="badge bg-success">จัดการข้อมูลพนักงานรายบุคคล</span>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover align-middle mb-0">
                                <thead class="table-light">
                                    <tr>
                                        <th>รหัสพนักงาน</th>
                                        <th>ชื่อ-นามสกุล / แผนก</th>
                                        <th class="text-center">โควตาวันลา (ใช้ไป / ทั้งหมด)</th>
                                        <th class="text-center" style="width: 170px;">จัดการผู้ใช้</th>
                                    </tr>
                                </thead>
                                <tbody id="approverSummaryTable">
                                    <!-- Dynamic -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Leave Requests Table for Approver -->
                <div class="card" id="pendingRequestsCard">
                    <div class="card-header d-flex justify-content-between align-items-center py-3">
                        <span><i class="bi bi-list-check me-2"></i> รายการคำขอลางานและคำขอคืนวันลาภายในบริษัท</span>
                        <div>
                            <span id="pendingBadgeCount" class="badge bg-danger rounded-pill px-2 py-1 me-2 shadow-sm" style="font-size: 0.85rem;">0 รายการรอตรวจสอบ</span>
                            <span class="badge bg-warning text-dark">รอตรวจสอบ</span>
                        </div>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover align-middle mb-0">
                                <thead class="table-dark">
                                    <tr>
                                        <th>รหัส</th>
                                        <th>บริษัท</th>
                                        <th>ชื่อ-นามสกุล / แผนก</th>
                                        <th>ประเภทการลา</th>
                                        <th>ช่วงวันที่ขอลา</th>
                                        <th>ผู้ปฏิบัติงานแทน</th>
                                        <th>สถานะปัจจุบัน</th>
                                        <th class="text-center">ตรวจสอบ & จัดการ</th>
                                    </tr>
                                </thead>
                                <tbody id="approverTable">
                                    <!-- Data rendered dynamically -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- MODAL: Add New Company Modal -->
    <div class="modal fade" id="addCompanyModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-building-add me-2"></i>เพิ่มบริษัทใหม่ในระบบ</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="addCompanyForm" onsubmit="handleAddNewCompany(event)">
                        <div class="mb-3">
                            <label class="form-label fw-bold">ชื่อบริษัท <span class="text-danger">*</span></label>
                            <input type="text" id="newCompanyName" class="form-control" placeholder="เช่น บริษัท นวัตกรรม ดิจิทัล จำกัด" required>
                        </div>
                        <div class="mb-3 p-3 bg-light rounded border">
                            <small class="text-muted d-block mb-1"><strong>ระบบจะสร้างให้อัตโนมัติ:</strong></small>
                            <ul class="small text-secondary mb-0 ps-3">
                                <li>ผู้อนุมัติหลัก (Main Approver)</li>
                                <li>รหัสผ่านเริ่มต้น: <strong>1234</strong></li>
                            </ul>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 fw-bold">บันทึกเพิ่มบริษัท</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Add New Approver Modal -->
    <div class="modal fade" id="addApproverModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-success text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-shield-plus me-2"></i>เพิ่มผู้อนุมัติใหม่ประจำบริษัท</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="addApproverForm" onsubmit="handleAddNewApprover(event)">
                        <div class="mb-3">
                            <label class="form-label fw-bold">ชื่อ-นามสกุลผู้อนุมัติ <span class="text-danger">*</span></label>
                            <input type="text" id="newApprName" class="form-control" placeholder="เช่น คุณสมชาย ผู้บริหาร" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">ตำแหน่ง / สิทธิ์ <span class="text-danger">*</span></label>
                            <input type="text" id="newApprPosition" class="form-control" placeholder="เช่น HR Manager / Assistant Director" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">รหัสผ่านสำหรับเข้าสู่ระบบ <span class="text-danger">*</span></label>
                            <input type="text" id="newApprPass" class="form-control" value="1234" required>
                        </div>
                        <button type="submit" class="btn btn-success w-100 fw-bold">บันทึกเพิ่มผู้อนุมัติใหม่</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Holiday Management Modal -->
    <div class="modal fade" id="holidayModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-info text-dark">
                    <h5 class="modal-title fw-bold"><i class="bi bi-calendar-event me-2"></i>จัดการวันหยุดนักขัตฤกษ์ประจำปี (Dynamic Holidays)</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-4 p-3 bg-light rounded border">
                        <h6 class="fw-bold text-primary mb-2"><i class="bi bi-plus-circle me-1"></i> เพิ่มวันหยุดนักขัตฤกษ์ใหม่</h6>
                        <form onsubmit="handleAddNewHoliday(event)">
                            <div class="row g-2">
                                <div class="col-md-5">
                                    <label class="form-label small fw-bold">ชื่อวันหยุด (เช่น วันสงกรานต์):</label>
                                    <input type="text" id="newHolidayName" class="form-control" placeholder="ระบุชื่อวันหยุด" required>
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold">วันที่หยุด:</label>
                                    <input type="date" id="newHolidayDate" class="form-control" required>
                                </div>
                                <div class="col-md-3 d-flex align-items-end">
                                    <button type="submit" class="btn btn-primary w-100 fw-bold">บันทึกวันหยุด</button>
                                </div>
                            </div>
                        </form>
                    </div>

                    <h6 class="fw-bold mb-2">รายการวันหยุดนักขัตฤกษ์ของบริษัทในปีนี้:</h6>
                    <div class="table-responsive">
                        <table class="table table-bordered table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th>วันที่</th>
                                    <th>ชื่อวันหยุดนักขัตฤกษ์</th>
                                    <th class="text-center" style="width: 100px;">จัดการ</th>
                                </tr>
                            </thead>
                            <tbody id="holidaysTableBody">
                                <!-- Dynamic -->
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ปิดหน้าต่าง</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Smart Capacity & Overlap Warning Modal -->
    <div class="modal fade" id="smartWarningModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content shadow-lg border-warning border-3">
                <div class="modal-header bg-warning text-dark">
                    <h5 class="modal-title fw-bold"><i class="bi bi-exclamation-triangle-fill me-2"></i>คำเตือน: กระทบอัตรากำลังพลในแผนก (>50%)</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-4">
                    <div class="alert alert-warning mb-3">
                        <strong>แจ้งเตือนอัจฉริยะ (Smart Capacity Warning):</strong><br>
                        คำเตือน: มีพนักงานในแผนกเดียวกันลาในช่วงเวลานี้จำนวนมาก อาจส่งผลกระทบต่อการปฏิบัติงาน
                    </div>
                    <p class="mb-2 text-secondary small" id="warningDetailList">-</p>
                    <p class="mb-0 fw-bold text-dark">คุณต้องการยืนยันส่งคำขอนี้ต่อหรือไม่?</p>
                </div>
                <div class="modal-footer bg-light">
                    <button type="button" class="btn btn-secondary px-4" data-bs-dismiss="modal">แก้ไข / เปลี่ยนแปลงวันลา</button>
                    <button type="button" class="btn btn-warning fw-bold text-dark px-4" onclick="confirmForceSubmitLeave()">ยืนยันส่งคำขอต่อไป</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL 1: Details & Approval Modal -->
    <div class="modal fade" id="detailModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title fw-bold" id="detailModalTitle">
                        <i class="bi bi-person-vcard me-2"></i> รายละเอียดคำขอลางาน
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-4">
                    <div class="row g-3">
                        <div class="col-md-6 border-end">
                            <h6 class="text-primary fw-bold mb-3"><i class="bi bi-person-circle me-1"></i> ข้อมูลพนักงาน</h6>
                            <p class="mb-1"><strong>สังกัดบริษัท:</strong> <span id="modalCompName" class="text-primary fw-bold">-</span></p>
                            <p class="mb-1"><strong>ชื่อ-นามสกุล:</strong> <span id="modalEmpName">-</span></p>
                            <p class="mb-1"><strong>รหัสพนักงาน:</strong> <span id="modalEmpId">-</span></p>
                            <p class="mb-1"><strong>แผนก:</strong> <span id="modalEmpDept">-</span></p>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-primary fw-bold mb-3"><i class="bi bi-file-text me-1"></i> รายละเอียดการลา</h6>
                            <p class="mb-1"><strong>ประเภทการลา:</strong> <span id="modalLeaveType" class="fw-bold text-dark">-</span></p>
                            <p class="mb-1"><strong>วันที่เริ่ม:</strong> <span id="modalStartDate">-</span></p>
                            <p class="mb-1"><strong>วันที่สิ้นสุด:</strong> <span id="modalEndDate">-</span></p>
                            <p class="mb-1"><strong>จำนวนวันลาคำนวณจริง:</strong> <span id="modalTotalDays" class="badge bg-primary fs-6">-</span></p>
                            <p class="mb-1 mt-2"><strong>เหตุผลประกอบ:</strong> <span id="modalReason" class="text-danger">-</span></p>
                            
                            <div class="p-2 bg-light rounded border my-2">
                                <small class="d-block text-primary fw-bold"><i class="bi bi-people-fill me-1"></i> ผู้ปฏิบัติงานแทน (Handover):</small>
                                <span id="modalHandover" class="text-dark fw-bold">-</span>
                                <div id="modalHandoverNotesBox" class="text-secondary small mt-1"></div>
                            </div>

                            <div id="modalCancelReasonBox" class="mb-1 mt-2 d-none">
                                <strong>เหตุผลที่ขอยกเลิก/คืนวันลา:</strong> <span id="modalCancelReason" class="text-warning fw-bold">-</span>
                            </div>
                            <div class="mb-1 mt-3 p-2 bg-light rounded border">
                                <strong>เอกสารแนบประกอบ:</strong> 
                                <div id="modalFile" class="mt-2">-</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer bg-light" id="detailModalFooter">
                    <!-- Dynamic Buttons -->
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Cancel Reason Input Modal -->
    <div class="modal fade" id="employeeCancelReasonModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-warning text-dark">
                    <h5 class="modal-title fw-bold"><i class="bi bi-arrow-counterclockwise me-2"></i>เหตุผลในการขอยกเลิก / ขอคืนวันลา</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <input type="hidden" id="cancelRequestIdInput">
                    <div class="mb-3">
                        <label class="form-label fw-bold">กรุณาระบุสาเหตุที่ต้องการยกเลิกวันลานี้:</label>
                        <textarea id="employeeCancelReasonText" class="form-control" rows="3" placeholder="เช่น หายป่วยก่อนกำหนด, เปลี่ยนแปลงแผนงานเดินทาง..."></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ปิด</button>
                    <button type="button" class="btn btn-warning fw-bold text-dark" onclick="submitEmployeeCancelRequest()">ส่งคำขอคืนวันลาให้ HR</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Email Notification Simulation Modal -->
    <div class="modal fade" id="emailSimulationModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content shadow-lg border-0">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-envelope-at-fill text-info me-2"></i>จำลองการส่งอีเมลแจ้งเตือน (Email Simulation)</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-4 bg-light">
                    <div class="card p-3 shadow-sm border">
                        <div class="mb-2 border-bottom pb-2">
                            <small class="text-muted d-block"><strong>To:</strong> <span id="simEmailTo" class="text-dark fw-bold">-</span></small>
                            <small class="text-muted d-block"><strong>From:</strong> system.leave@company-group.co.th</small>
                            <small class="text-muted d-block"><strong>Subject:</strong> <span id="simEmailSubject" class="text-primary fw-bold">-</span></small>
                        </div>
                        <div class="py-2">
                            <p class="mb-2" id="simGreeting">เรียน คุณ <span id="simEmpName" class="fw-bold">-</span>,</p>
                            <p id="simEmailMessage" class="mb-3 text-secondary p-2 bg-white rounded border">-</p>
                            <div class="small text-muted" id="simFooterDetails">
                                รายละเอียด: <span id="simLeaveDetails" class="fw-bold text-dark">-</span><br>
                                ดำเนินการโดย: <span id="simApproverName" class="fw-bold text-dark">-</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer bg-white">
                    <button type="button" class="btn btn-primary w-100 fw-bold" data-bs-dismiss="modal">
                        <i class="bi bi-send-check me-1"></i> รับทราบ (จำลองส่งอีเมลสำเร็จเรียบร้อย)
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Document Preview Modal -->
    <div class="modal fade" id="docPreviewModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-xl">
            <div class="modal-content">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-eye me-2"></i>ตัวอย่างเอกสารแนบ: <span id="previewFileName" class="text-info"></span></h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body text-center bg-secondary bg-opacity-10 p-3" style="min-height: 500px; display: flex; align-items: center; justify-content: center;">
                    <div id="previewContainer" style="width: 100%; height: 100%;">
                        <!-- Dynamic Preview Content -->
                    </div>
                </div>
                <div class="modal-footer">
                    <a id="previewDownloadBtn" href="#" target="_blank" class="btn btn-primary">
                        <i class="bi bi-download me-1"></i> ดาวน์โหลดไฟล์จริง
                    </a>
                    <button type="button" class="btn btn-secondary" onclick="closePreviewModal()">ปิดหน้าต่างพรีวิว</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Add New Employee Modal -->
    <div class="modal fade" id="addEmployeeModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-person-plus-fill me-2"></i>ลงทะเบียนพนักงานใหม่</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="addEmployeeForm" onsubmit="handleAddNewEmployee(event)">
                        <div class="mb-3">
                            <label class="form-label fw-bold">ชื่อ-นามสกุลพนักงาน <span class="text-danger">*</span></label>
                            <input type="text" id="newEmpName" class="form-control" placeholder="เช่น นายสมศักดิ์ รักงาน" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">แผนก / ฝ่าย <span class="text-danger">*</span></label>
                            <input type="text" id="newEmpDept" class="form-control" placeholder="เช่น ฝ่ายการตลาดดิจิทัล" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">รหัสพนักงาน</label>
                            <input type="text" id="newEmpId" class="form-control" placeholder="เช่น EMP100">
                        </div>
                        <div class="mb-3 p-3 bg-light rounded border">
                            <label class="form-label fw-bold small text-secondary mb-1">รหัสผ่านเริ่มต้นสำหรับเข้าสู่ระบบ:</label>
                            <input type="text" class="form-control form-control-sm" value="1234 (ค่ามาตรฐาน)" disabled>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 fw-bold">บันทึกเพิ่มพนักงานใหม่</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Change Password Modal -->
    <div class="modal fade" id="changePasswordModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-key-fill me-2"></i>เปลี่ยนรหัสผ่านพนักงาน</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <input type="hidden" id="resetPassEmpId">
                    <p class="mb-3">พนักงาน: <strong id="resetPassEmpName" class="text-primary"></strong></p>
                    <div class="mb-3">
                        <label class="form-label fw-bold">รหัสผ่านใหม่ <span class="text-danger">*</span></label>
                        <input type="text" id="newPasswordInput" class="form-control" placeholder="กรอกรหัสผ่านใหม่ (เช่น 1234 หรือรหัสอื่นๆ)" required>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ยกเลิก</button>
                    <button type="button" class="btn btn-dark" onclick="saveNewPassword()">บันทึกรหัสผ่านใหม่</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Reject Reason Input Modal -->
    <div class="modal fade" id="rejectReasonModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-danger text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-exclamation-octagon me-2"></i>ระบุเหตุผลในการไม่อนุมัติ (Reject)</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label fw-bold">กรุณาระบุสาเหตุหรือข้อเสนอแนะ:</label>
                        <textarea id="rejectionReasonInput" class="form-control" rows="3" placeholder="เช่น งานด่วนติดช่วงนั้น, เอกสารใบรับรองแพทย์ไม่ชัดเจน..."></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ยกเลิก</button>
                    <button type="button" class="btn btn-danger" onclick="confirmRejectWithReason()">ยืนยันปฏิเสธคำขอ</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL 2: Edit Employee Quota Modal -->
    <div class="modal fade" id="editQuotaModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-success text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-sliders me-2"></i>แก้ไขโควตาวันลาพนักงาน</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <input type="hidden" id="editQuotaEmpId">
                    <p class="mb-3">พนักงาน: <strong id="editQuotaEmpName" class="text-primary"></strong></p>
                    <div id="editQuotaFieldsContainer" class="vstack gap-3">
                        <!-- Dynamic quota inputs will be generated here -->
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ยกเลิก</button>
                    <button type="button" class="btn btn-success" onclick="saveEmployeeQuotaChanges()">บันทึกการเปลี่ยนแปลง</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL 3: Leave Type Configuration Modal -->
    <div class="modal fade" id="leaveTypeConfigModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-gear-fill me-2"></i>จัดการประเภทการลาทั้งหมดในระบบ</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-4 p-3 bg-light rounded border">
                        <h6 class="fw-bold text-primary mb-2"><i class="bi bi-plus-circle me-1"></i> เพิ่มประเภทการลาใหม่</h6>
                        <div class="row g-2">
                            <div class="col-md-5">
                                <input type="text" id="newLeaveTypeName" class="form-control" placeholder="ชื่อประเภทการลา (เช่น ลาศึกษาต่อ, ลาบวช)">
                            </div>
                            <div class="col-md-4">
                                <input type="number" id="newLeaveTypeDefaultQuota" class="form-control" placeholder="โควตาเริ่มต้น (วัน)" min="1" value="10">
                            </div>
                            <div class="col-md-3">
                                <button type="button" class="btn btn-primary w-100 fw-bold" onclick="addNewLeaveType()">เพิ่มประเภท</button>
                            </div>
                        </div>
                    </div>

                    <h6 class="fw-bold mb-2">ประเภทการลาที่มีอยู่ทั้งหมดในระบบ:</h6>
                    <div class="table-responsive">
                    <table class="table table-bordered table-hover align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th>ชื่อประเภทการลา</th>
                                <th class="text-center">โควตาตั้งต้นมาตรฐาน</th>
                                <th class="text-center" style="width: 100px;">จัดการ</th>
                            </tr>
                        </thead>
                        <tbody id="leaveTypesConfigTable">
                            <!-- Dynamic -->
                        </tbody>
                    </table>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ปิดหน้าต่าง</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL 4: Reset Quota Confirmation -->
    <div class="modal fade" id="resetModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-warning text-dark">
                    <h5 class="modal-title fw-bold"><i class="bi bi-exclamation-triangle-fill me-2"></i>ยืนยันการรีเซ็ตสิทธิวันลา</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p class="mb-2">คุณกำลังจะทำการรีเซ็ตประวัติการใช้สิทธิวันลาให้กลับเป็น 0 สำหรับพนักงานทุกคน</p>
                    <p class="text-danger small mb-0"><strong>คำเตือน:</strong> รายการประวัติคำขอลางานทั้งหมดจะถูกล้างใหม่</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ยกเลิก</button>
                    <button type="button" class="btn btn-danger" onclick="confirmResetQuota()">ยืนยันการรีเซ็ต</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap 5 JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        const defaultLeaveTypes = {
            "ลาพักร้อน": { name: "ลาพักร้อน", defaultQuota: 10, color: "text-primary" },
            "ลาป่วย": { name: "ลาป่วย", defaultQuota: 30, color: "text-success" },
            "ลากิจ": { name: "ลากิจ", defaultQuota: 6, color: "text-warning" }
        };

        const defaultCompanies = {
            "COMP01": "บริษัท เทคโนโลยี นวัตกรรม จำกัด",
            "COMP02": "บริษัท การตลาด สร้างสรรค์ จำกัด",
            "COMP03": "บริษัท การเงิน มั่นคง จำกัด",
            "COMP04": "บริษัท ดีไซน์ สตูดิโอ จำกัด",
            "COMP05": "บริษัท โลจิสติกส์ ไทย จำกัด"
        };

        const defaultApprovers = {
            "APPR001_1": { id: "APPR001_1", companyId: "COMP01", name: "ดร.วิกรม นวัตกรรม", position: "ผู้จัดการทั่วไป (Main Approver)", pass: "1234" },
            "APPR001_2": { id: "APPR001_2", companyId: "COMP01", name: "คุณกุลธิดา รองผู้จัดการ", position: "รองผู้จัดการ (Backup Approver)", pass: "1234" },
            "APPR002_1": { id: "APPR002_1", companyId: "COMP02", name: "คุณวิภาดา การตลาด", position: "ผู้อำนวยการ (Main Approver)", pass: "1234" },
            "APPR003_1": { id: "APPR003_1", companyId: "COMP03", name: "คุณสมศักดิ์ การเงิน", position: "CFO (Main Approver)", pass: "1234" },
            "APPR004_1": { id: "APPR004_1", companyId: "COMP04", name: "คุณณัฐกาญจน์ ดีไซน์", position: "ผู้อำนวยการ (Main Approver)", pass: "1234" },
            "APPR005_1": { id: "APPR005_1", companyId: "COMP05", name: "คุณเกรียงไกร โลจิสติกส์", position: "ผู้จัดการ (Main Approver)", pass: "1234" }
        };

        const defaultEmployees = {
            "EMP001": { id: "EMP001", companyId: "COMP01", name: "นายสมชาย สายชิว", dept: "ฝ่ายพัฒนาระบบ", pass: "1234", email: "somchai@company.co.th", quotas: { "ลาพักร้อน": {total: 12, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP002": { id: "EMP002", companyId: "COMP01", name: "นายวิชัย ใจดี", dept: "ฝ่ายพัฒนาระบบ", pass: "1234", email: "wichai@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP004": { id: "EMP004", companyId: "COMP02", name: "นางสาวสมหญิง จริงใจ", dept: "ฝ่ายวางแผนสื่อ", pass: "1234", email: "somying@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP007": { id: "EMP007", companyId: "COMP03", name: "นายธีรภัทร ยอดเยี่ยม", dept: "ฝ่ายบัญชีการเงิน", pass: "1234", email: "theerapat@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP010": { id: "EMP010", companyId: "COMP04", name: "นายกิตติ ศิลป์งาม", dept: "ฝ่าย Design", pass: "1234", email: "kitti@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP013": { id: "EMP013", companyId: "COMP05", name: "นางสาวศิริพร ว่องไว", dept: "ฝ่ายคลังสินค้า", pass: "1234", email: "siriporn@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } }
        };

        const defaultHolidays = [
            { id: "H01", companyId: "COMP01", date: "2026-01-01", name: "วันขึ้นปีใหม่" },
            { id: "H02", companyId: "COMP01", date: "2026-04-13", name: "วันสงกรานต์" },
            { id: "H03", companyId: "COMP01", date: "2026-04-14", name: "วันสงกรานต์" },
            { id: "H04", companyId: "COMP01", date: "2026-04-15", name: "วันสงกรานต์" },
            { id: "H05", companyId: "COMP01", date: "2026-05-01", name: "วันแรงงานแห่งชาติ" },
            { id: "H06", companyId: "COMP01", date: "2026-07-28", name: "วันเฉลิมพระชนมพรรษา ร.10" },
            { id: "H07", companyId: "COMP01", date: "2026-08-12", name: "วันแม่แห่งชาติ" },
            { id: "H08", companyId: "COMP01", date: "2026-12-05", name: "วันพ่อแห่งชาติ" },
            { id: "H09", companyId: "COMP01", date: "2026-12-31", name: "วันสิ้นปี" }
        ];

        let activeLeaveIdForApproval = null;
        let currentActiveFileData = null;
        let currentActiveFileName = null;
        let currentManagingCompanyId = null;
        let pendingLeavePayload = null;

        let calendarYear = new Date().getFullYear();
        let calendarMonth = new Date().getMonth();

        function initData() {
            if (!localStorage.getItem("v25_leaveTypes")) {
                localStorage.setItem("v25_leaveTypes", JSON.stringify(defaultLeaveTypes));
                localStorage.setItem("v25_companies", JSON.stringify(defaultCompanies));
                localStorage.setItem("v25_approvers", JSON.stringify(defaultApprovers));
                localStorage.setItem("v25_employees", JSON.stringify(defaultEmployees));
                localStorage.setItem("v25_leaveRequests", JSON.stringify([]));
                localStorage.setItem("v25_holidays", JSON.stringify(defaultHolidays));
            }
            populateLoginDropdowns();
            checkSession();
        }

        function getLeaveTypes() { return JSON.parse(localStorage.getItem("v25_leaveTypes")); }
        function saveLeaveTypes(data) { localStorage.setItem("v25_leaveTypes", JSON.stringify(data)); }
        function getCompanies() { return JSON.parse(localStorage.getItem("v25_companies")); }
        function saveCompanies(data) { localStorage.setItem("v25_companies", JSON.stringify(data)); }
        function getApprovers() { return JSON.parse(localStorage.getItem("v25_approvers")); }
        function saveApprovers(data) { localStorage.setItem("v25_approvers", JSON.stringify(data)); }
        function getEmployees() { return JSON.parse(localStorage.getItem("v25_employees")); }
        function saveEmployees(data) { localStorage.setItem("v25_employees", JSON.stringify(data)); }
        function getRequests() { return JSON.parse(localStorage.getItem("v25_leaveRequests")); }
        function saveRequests(data) { localStorage.setItem("v25_leaveRequests", JSON.stringify(data)); }
        function getHolidays() { return JSON.parse(localStorage.getItem("v25_holidays") || "[]"); }
        function saveHolidays(data) { localStorage.setItem("v25_holidays", JSON.stringify(data)); }
        function getSession() { return JSON.parse(localStorage.getItem("v25_session")); }
        function saveSession(session) { localStorage.setItem("v25_session", JSON.stringify(session)); }

        function populateLoginDropdowns() {
            const companies = getCompanies();
            const empCompSelect = document.getElementById("loginCompanySelect");
            const apprCompSelect = document.getElementById("loginApprCompanySelect");
            
            empCompSelect.innerHTML = "";
            apprCompSelect.innerHTML = "";

            let firstCId = null;
            let count = 0;
            for (let cId in companies) {
                if (count === 0) firstCId = cId;
                empCompSelect.innerHTML += `<option value="${cId}">${companies[cId]}</option>`;
                apprCompSelect.innerHTML += `<option value="${cId}">${companies[cId]}</option>`;
                count++;
            }
            if (firstCId) {
                onLoginCompanyChange(firstCId);
                onLoginApprCompanyChange(firstCId);
            }
        }

        function onLoginCompanyChange(cId) {
            const employees = getEmployees();
            const userSelect = document.getElementById("loginUserSelect");
            userSelect.innerHTML = "";

            let hasEmp = false;
            for (let eId in employees) {
                if (employees[eId].companyId === cId) {
                    hasEmp = true;
                    userSelect.innerHTML += `<option value="${eId}">${employees[eId].name} (${employees[eId].dept})</option>`;
                }
            }
            if (!hasEmp) {
                userSelect.innerHTML = `<option value="">-- ยังไม่มีพนักงานในบริษัทนี้ --</option>`;
            }
        }

        function onLoginApprCompanyChange(cId) {
            const approvers = getApprovers();
            const apprSelect = document.getElementById("loginApprUserSelect");
            apprSelect.innerHTML = "";

            let hasAppr = false;
            for (let aId in approvers) {
                if (approvers[aId].companyId === cId) {
                    hasAppr = true;
                    apprSelect.innerHTML += `<option value="${aId}">${approvers[aId].name} - ${approvers[aId].position}</option>`;
                }
            }
            if (!hasAppr) {
                apprSelect.innerHTML = `<option value="">-- ยังไม่มีผู้อนุมัติในบริษัทนี้ --</option>`;
            }
        }

        function openAddCompanyModal() {
            document.getElementById("addCompanyForm").reset();
            const modal = new bootstrap.Modal(document.getElementById('addCompanyModal'));
            modal.show();
        }

        function handleAddNewCompany(e) {
            e.preventDefault();
            const compNameInput = document.getElementById("newCompanyName").value.trim();
            if (!compNameInput) return;

            let companies = getCompanies();
            const newCompId = "COMP" + Date.now().toString().slice(-4);

            companies[newCompId] = compNameInput;
            saveCompanies(companies);

            // สร้างผู้อนุมัติเริ่มต้นประจำบริษัทใหม่
            let approvers = getApprovers();
            const newApprId = `APPR_${newCompId}_1`;
            approvers[newApprId] = {
                id: newApprId,
                companyId: newCompId,
                name: `ผู้บริหาร ${compNameInput}`,
                position: "General Manager (Approver)",
                pass: "1234"
            };
            saveApprovers(approvers);

            // สร้างพนักงานเริ่มต้นให้ 1 คนในบริษัทใหม่
            let employees = getEmployees();
            const newEmpId = "EMP" + Date.now().toString().slice(-4);
            const leaveTypes = getLeaveTypes();
            let defaultQuotas = {};
            for (let lKey in leaveTypes) {
                defaultQuotas[lKey] = { total: leaveTypes[lKey].defaultQuota, used: 0 };
            }

            employees[newEmpId] = {
                id: newEmpId,
                companyId: newCompId,
                name: "พนักงานทดสอบ ระบบ",
                dept: "ฝ่ายบริหารทั่วไป",
                pass: "1234",
                email: newEmpId.toLowerCase() + "@company.co.th",
                quotas: defaultQuotas
            };
            saveEmployees(employees);

            const modalEl = document.getElementById('addCompanyModal');
            const modalInstance = bootstrap.Modal.getInstance(modalEl);
            if (modalInstance) modalInstance.hide();

            populateLoginDropdowns();
            
            document.getElementById("loginApprCompanySelect").value = newCompId;
            onLoginApprCompanyChange(newCompId);
            document.getElementById("loginCompanySelect").value = newCompId;
            onLoginCompanyChange(newCompId);

            alert(`เพิ่มบริษัท "${compNameInput}" เรียบร้อยแล้ว!\n(ระบบได้สร้างผู้อนุมัติและพนักงานเริ่มต้นให้ พร้อมรหัสผ่าน: 1234)`);
        }

        function openAddApproverModal() {
            document.getElementById("addApproverForm").reset();
            document.getElementById("newApprPass").value = "1234";
            const modal = new bootstrap.Modal(document.getElementById('addApproverModal'));
            modal.show();
        }

        function handleAddNewApprover(e) {
            e.preventDefault();
            const name = document.getElementById("newApprName").value.trim();
            const position = document.getElementById("newApprPosition").value.trim();
            const pass = document.getElementById("newApprPass").value.trim();

            if (!name || !position || !pass) {
                alert("กรุณากรอกข้อมูลให้ครบถ้วน");
                return;
            }

            let approvers = getApprovers();
            const newApprId = "APPR_" + currentManagingCompanyId + "_" + Date.now().toString().slice(-4);

            approvers[newApprId] = {
                id: newApprId,
                companyId: currentManagingCompanyId,
                name: name,
                position: position,
                pass: pass
            };

            saveApprovers(approvers);
            bootstrap.Modal.getInstance(document.getElementById('addApproverModal')).hide();
            alert(`เพิ่มผู้อนุมัติใหม่ "${name}" (${position}) เรียบร้อยแล้ว!`);
            populateLoginDropdowns();
        }

        function handleEmployeeLogin(e) {
            e.preventDefault();
            const empId = document.getElementById("loginUserSelect").value;
            if (!empId) {
                alert("กรุณาเลือกพนักงานที่ต้องการเข้าสู่ระบบ");
                return;
            }
            const pass = document.getElementById("empPassword").value;
            const employees = getEmployees();
            const emp = employees[empId];

            const correctPass = emp ? (emp.pass || "1234") : "1234";
            if (pass !== correctPass) {
                alert("รหัสผ่านไม่ถูกต้อง! (รหัสผ่านเริ่มต้นคือ 1234)");
                return;
            }

            saveSession({ role: "employee", empId: empId });
            document.getElementById("empPassword").value = "";
            checkSession();
        }

        function handleApproverLogin(e) {
            e.preventDefault();
            const apprId = document.getElementById("loginApprUserSelect").value;
            if (!apprId) {
                alert("กรุณาเลือกผู้อนุมัติ");
                return;
            }
            const pass = document.getElementById("apprPassword").value;
            const approvers = getApprovers();
            const apprObj = approvers[apprId];

            const correctPass = apprObj ? (apprObj.pass || "1234") : "1234";

            if (pass !== correctPass) {
                alert("รหัสผ่านไม่ถูกต้อง! (รหัสผ่านเริ่มต้นคือ 1234)");
                return;
            }

            saveSession({ role: "approver", apprId: apprId });
            document.getElementById("apprPassword").value = "";
            checkSession();
        }

        function handleLogout() {
            localStorage.removeItem("v25_session");
            checkSession();
        }

        function checkSession() {
            const session = getSession();
            const loginView = document.getElementById("loginView");
            const appView = document.getElementById("appView");
            const empSection = document.getElementById("employeeSection");
            const apprSection = document.getElementById("approverSection");

            if (!session) {
                loginView.classList.remove("d-none");
                appView.classList.add("d-none");
            } else {
                loginView.classList.add("d-none");
                appView.classList.remove("d-none");

                if (session.role === "employee") {
                    empSection.classList.remove("d-none");
                    apprSection.classList.add("d-none");
                    renderEmployeeView(session.empId);
                } else if (session.role === "approver") {
                    empSection.classList.add("d-none");
                    apprSection.classList.remove("d-none");
                    renderApproverView(session.apprId);
                }
            }
        }

        function renderEmployeeView(empId) {
            const employees = getEmployees();
            const companies = getCompanies();
            const emp = employees[empId];

            if (!emp) {
                handleLogout();
                return;
            }

            document.getElementById("navUserName").innerText = emp.name;
            document.getElementById("navUserRole").innerText = "สิทธิ์: พนักงาน";

            document.getElementById("empInfoCompany").innerText = companies[emp.companyId] || "บริษัท";
            document.getElementById("empInfoName").innerText = emp.name;
            document.getElementById("empInfoDept").innerText = `รหัส: ${emp.id} | แผนก: ${emp.dept}`;

            const handoverSelect = document.getElementById("handoverColleague");
            handoverSelect.innerHTML = `<option value="-">-- เลือกเพื่อนร่วมงานปฏิบัติงานแทน (ไม่ระบุได้) --</option>`;
            for (let eId in employees) {
                if (employees[eId].companyId === emp.companyId && eId !== emp.id) {
                    handoverSelect.innerHTML += `<option value="${employees[eId].name} (${employees[eId].dept})">${employees[eId].name} (${employees[eId].dept})</option>`;
                }
            }

            const quotaGrid = document.getElementById("empQuotaDisplayGrid");
            quotaGrid.innerHTML = "";
            const leaveTypes = getLeaveTypes();

            for (let lKey in leaveTypes) {
                if (!emp.quotas[lKey]) {
                    emp.quotas[lKey] = { total: leaveTypes[lKey].defaultQuota, used: 0 };
                }
                const q = emp.quotas[lKey];
                quotaGrid.innerHTML += `
                    <div>
                        <span class="d-block text-muted small">${lKey}</span>
                        <span class="fw-bold ${leaveTypes[lKey].color || 'text-primary'} fs-5">${q.used}/${q.total} วัน</span>
                    </div>
                    <div class="border-start pe-2"></div>
                `;
            }

            const leaveTypeSelect = document.getElementById("leaveType");
            leaveTypeSelect.innerHTML = `<option value="">-- กรุณาเลือกประเภทการลา --</option>`;
            for (let lKey in leaveTypes) {
                leaveTypeSelect.innerHTML += `<option value="${lKey}">${leaveTypes[lKey].name}</option>`;
            }

            document.getElementById("modeFull").checked = true;
            onDurationModeChange();

            renderEmployeeHistory(empId);
        }

        function onDurationModeChange() {
            const isHalf = document.getElementById("modeHalf").checked;
            const sessionContainer = document.getElementById("halfDaySessionContainer");
            const endDateContainer = document.getElementById("endDateColContainer");
            const startDateLabel = document.getElementById("startDateLabel");
            const endDateInput = document.getElementById("endDate");

            if (isHalf) {
                sessionContainer.classList.remove("d-none");
                endDateContainer.classList.add("d-none");
                startDateLabel.innerText = "วันที่ต้องการลาครึ่งวัน *";
                endDateInput.removeAttribute("required");
                endDateInput.value = document.getElementById("startDate").value;
            } else {
                sessionContainer.classList.add("d-none");
                endDateContainer.classList.remove("d-none");
                startDateLabel.innerText = "วันที่เริ่มต้น *";
                endDateInput.setAttribute("required", "true");
            }
            calculateDays();
        }

        function renderApproverView(apprId) {
            const approvers = getApprovers();
            const companies = getCompanies();
            const apprObj = approvers[apprId] || { name: "ผู้อนุมัติ", position: "ผู้จัดการ", companyId: "COMP01" };
            const companyId = apprObj.companyId;

            currentManagingCompanyId = companyId;

            document.getElementById("navUserName").innerText = apprObj.name;
            document.getElementById("navUserRole").innerText = `${apprObj.position} | ${companies[companyId] || ''}`;
            document.getElementById("approverCompanyText").innerText = companies[companyId] || 'บริษัท';

            renderTeamCalendar();
            renderApproverSummary(companyId);
            renderApproverTable(companyId);
        }

        function changeCalendarMonth(direction) {
            calendarMonth += direction;
            if (calendarMonth > 11) {
                calendarMonth = 0;
                calendarYear++;
            } else if (calendarMonth < 0) {
                calendarMonth = 11;
                calendarYear--;
            }
            renderTeamCalendar();
        }

        function renderTeamCalendar() {
            const tbody = document.getElementById("teamCalendarBody");
            const label = document.getElementById("currentCalendarMonthLabel");
            if (!tbody || !label) return;

            const thaiMonths = [
                "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
                "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
            ];

            label.innerText = `${thaiMonths[calendarMonth]} พ.ศ. ${calendarYear + 543}`;

            const firstDayIndex = new Date(calendarYear, calendarMonth, 1).getDay();
            const totalDaysInMonth = new Date(calendarYear, calendarMonth + 1, 0).getDate();
            const prevMonthDays = new Date(calendarYear, calendarMonth, 0).getDate();

            const requests = getRequests().filter(r => r.companyId === currentManagingCompanyId && (r.status === "Approved" || r.status === "Pending"));
            const holidays = getHolidays().filter(h => h.companyId === currentManagingCompanyId);

            let leaveDaysMap = {};
            requests.forEach(req => {
                let cur = new Date(req.startDate);
                let end = new Date(req.endDate);
                while (cur <= end) {
                    const y = cur.getFullYear();
                    const m = String(cur.getMonth() + 1).padStart(2, '0');
                    const d = String(cur.getDate()).padStart(2, '0');
                    const dateStr = `${y}-${m}-${d}`;

                    if (!leaveDaysMap[dateStr]) leaveDaysMap[dateStr] = { leaves: [], holidays: [] };
                    leaveDaysMap[dateStr].leaves.push({ name: req.empName, type: req.type, status: req.status, isHalf: req.isHalf, halfSession: req.halfSession });

                    cur.setDate(cur.getDate() + 1);
                }
            });

            holidays.forEach(h => {
                if (!leaveDaysMap[h.date]) leaveDaysMap[h.date] = { leaves: [], holidays: [] };
                leaveDaysMap[h.date].holidays.push(h.name);
            });

            tbody.innerHTML = "";
            let dateTracker = 1;
            let nextMonthDayTracker = 1;
            const todayStr = new Date().toISOString().split('T')[0];

            for (let row = 0; row < 6; row++) {
                let tr = document.createElement("tr");
                let hasDaysInWeek = false;

                for (let col = 0; col < 7; col++) {
                    let td = document.createElement("td");
                    td.className = "calendar-cell p-2 border";

                    if (row === 0 && col < firstDayIndex) {
                        td.classList.add("other-month");
                        let prevDay = prevMonthDays - (firstDayIndex - col - 1);
                        td.innerHTML = `<span class="fw-bold text-muted">${prevDay}</span>`;
                    } else if (dateTracker > totalDaysInMonth) {
                        td.classList.add("other-month");
                        td.innerHTML = `<span class="fw-bold text-muted">${nextMonthDayTracker}</span>`;
                        nextMonthDayTracker++;
                    } else {
                        hasDaysInWeek = true;
                        const mStr = String(calendarMonth + 1).padStart(2, '0');
                        const dStr = String(dateTracker).padStart(2, '0');
                        const fullDateStr = `${calendarYear}-${mStr}-${dStr}`;

                        if (fullDateStr === todayStr) {
                            td.classList.add("today");
                        }

                        let cellHtml = `<div class="fw-bold mb-1">${dateTracker}</div>`;

                        if (leaveDaysMap[fullDateStr]) {
                            leaveDaysMap[fullDateStr].holidays.forEach(hName => {
                                cellHtml += `<span class="holiday-badge" title="วันหยุดนักขัตฤกษ์: ${hName}">🔴 ${hName}</span>`;
                            });

                            leaveDaysMap[fullDateStr].leaves.forEach(leave => {
                                let badgeBg = "bg-primary text-white";
                                if (leave.type === "ลาป่วย") badgeBg = "bg-success text-white";
                                else if (leave.type === "ลากิจ") badgeBg = "bg-warning text-dark";
                                if (leave.status === "Pending") badgeBg = "bg-secondary text-white opacity-75";

                                let subText = "";
                                if (leave.isHalf) {
                                    subText = leave.halfSession === "morning" ? " (เช้า)" : " (บ่าย)";
                                }

                                cellHtml += `<span class="leave-event-badge ${badgeBg}" title="${leave.name} (${leave.type}${subText})">👤 ${leave.name} (${leave.type}${subText})</span>`;
                            });
                        }

                        td.innerHTML = cellHtml;
                        dateTracker++;
                    }
                    tr.appendChild(td);
                }

                if (hasDaysInWeek || row < 4) {
                    tbody.appendChild(tr);
                }
            }
        }

        function openHolidayModal() {
            document.getElementById("newHolidayName").value = "";
            document.getElementById("newHolidayDate").value = "";
            renderHolidaysTable();
            const modal = new bootstrap.Modal(document.getElementById('holidayModal'));
            modal.show();
        }

        function renderHolidaysTable() {
            const tbody = document.getElementById("holidaysTableBody");
            const holidays = getHolidays().filter(h => h.companyId === currentManagingCompanyId);
            tbody.innerHTML = "";

            if (holidays.length === 0) {
                tbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted py-3">ยังไม่มีการบันทึกวันหยุดนักขัตฤกษ์ในบริษัทนี้</td></tr>`;
                return;
            }

            holidays.sort((a, b) => new Date(a.date) - new Date(b.date));

            holidays.forEach(h => {
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${h.date}</strong></td>
                        <td>${h.name}</td>
                        <td class="text-center">
                            <button class="btn btn-sm btn-outline-danger px-2 py-1" onclick="deleteHoliday('${h.id}')"><i class="bi bi-trash"></i> ลบ</button>
                        </td>
                    </tr>
                `;
            });
        }

        function handleAddNewHoliday(e) {
            e.preventDefault();
            const name = document.getElementById("newHolidayName").value.trim();
            const date = document.getElementById("newHolidayDate").value;

            if (!name || !date) {
                alert("กรุณากรอกข้อมูลให้ครบถ้วน");
                return;
            }

            let holidays = getHolidays();
            const newHoliday = {
                id: "HOL-" + Date.now().toString().slice(-5),
                companyId: currentManagingCompanyId,
                date: date,
                name: name
            };

            holidays.push(newHoliday);
            saveHolidays(holidays);

            document.getElementById("newHolidayName").value = "";
            document.getElementById("newHolidayDate").value = "";
            renderHolidaysTable();
            renderTeamCalendar();
            alert("เพิ่มวันหยุดนักขัตฤกษ์เรียบร้อยแล้ว");
        }

        function deleteHoliday(holidayId) {
            if (!confirm("คุณต้องการลบวันหยุดนักขัตฤกษ์นี้ใช่หรือไม่?")) return;
            let holidays = getHolidays().filter(h => h.id !== holidayId);
            saveHolidays(holidays);
            renderHolidaysTable();
            renderTeamCalendar();
            alert("ลบวันหยุดเรียบร้อยแล้ว");
        }

        function renderApproverSummary(approverCompanyId) {
            const employees = getEmployees();
            const leaveTypes = getLeaveTypes();
            const tbody = document.getElementById("approverSummaryTable");
            if (!tbody) return;
            tbody.innerHTML = "";

            let compEmployees = [];
            for (let eId in employees) {
                if (employees[eId].companyId === approverCompanyId) {
                    compEmployees.push(employees[eId]);
                }
            }

            if (compEmployees.length === 0) {
                tbody.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-3">ยังไม่มีพนักงานในบริษัทนี้ (สามารถกดเพิ่มพนักงานใหม่ได้ด้านบน)</td></tr>`;
                return;
            }

            compEmployees.forEach(emp => {
                let quotaBadgeHtml = "";
                for (let lKey in leaveTypes) {
                    if (!emp.quotas[lKey]) {
                        emp.quotas[lKey] = { total: leaveTypes[lKey].defaultQuota, used: 0 };
                    }
                    const q = emp.quotas[lKey];
                    const rem = (q.total - q.used).toFixed(1);
                    quotaBadgeHtml += `<div class="mb-1"><strong>${lKey}:</strong> <span class="text-primary fw-bold">${q.used}</span> / ${q.total} วัน <small class="text-muted">(เหลือ ${rem})</small></div>`;
                }

                tbody.innerHTML += `
                    <tr>
                        <td><strong>${emp.id}</strong><br><small class="text-muted">Password: ${emp.pass || '1234'}</small></td>
                        <td>${emp.name} <br><small class="text-muted">${emp.dept}</small></td>
                        <td>${quotaBadgeHtml}</td>
                        <td class="text-center">
                            <div class="vstack gap-1">
                                <button class="btn btn-sm btn-outline-success py-0" onclick="openEditQuotaModal('${emp.id}')"><i class="bi bi-sliders me-1"></i> โควตา</button>
                                <button class="btn btn-sm btn-outline-dark py-0" onclick="openChangePasswordModal('${emp.id}')"><i class="bi bi-key me-1"></i> เปลี่ยนรหัส</button>
                                <button class="btn btn-sm btn-outline-danger py-0" onclick="deleteEmployee('${emp.id}')"><i class="bi bi-trash me-1"></i> ลบพนักงาน</button>
                            </div>
                        </td>
                    </tr>
                `;
            });
        }

        function openAddEmployeeModal() {
            document.getElementById("addEmployeeForm").reset();
            document.getElementById("newEmpId").value = "EMP" + Math.floor(100 + Math.random() * 900);
            const modal = new bootstrap.Modal(document.getElementById('addEmployeeModal'));
            modal.show();
        }

        function handleAddNewEmployee(e) {
            e.preventDefault();
            const name = document.getElementById("newEmpName").value.trim();
            const dept = document.getElementById("newEmpDept").value.trim();
            let empId = document.getElementById("newEmpId").value.trim();

            if (!name || !dept) {
                alert("กรุณากรอกข้อมูลชื่อและแผนกให้ครบถ้วน");
                return;
            }

            let employees = getEmployees();
            if (!empId) {
                empId = "EMP" + Date.now().toString().slice(-4);
            }

            if (employees[empId]) {
                alert("รหัสพนักงานนี้มีอยู่ในระบบแล้ว กรุณาใช้รหัสอื่น");
                return;
            }

            const leaveTypes = getLeaveTypes();
            let defaultQuotas = {};
            for (let lKey in leaveTypes) {
                defaultQuotas[lKey] = { total: leaveTypes[lKey].defaultQuota, used: 0 };
            }

            employees[empId] = {
                id: empId,
                companyId: currentManagingCompanyId,
                name: name,
                dept: dept,
                pass: "1234",
                email: empId.toLowerCase() + "@company.co.th",
                quotas: defaultQuotas
            };

            saveEmployees(employees);
            bootstrap.Modal.getInstance(document.getElementById('addEmployeeModal')).hide();
            alert(`เพิ่มพนักงานใหม่ "${name}" (รหัส: ${empId}) เรียบร้อยแล้ว (รหัสผ่านเริ่มต้น: 1234)`);
            renderApproverView(getSession().apprId);
        }

        function openChangePasswordModal(empId) {
            const employees = getEmployees();
            const emp = employees[empId];
            if (!emp) return;

            document.getElementById("resetPassEmpId").value = empId;
            document.getElementById("resetPassEmpName").innerText = `${emp.name} (${emp.id})`;
            document.getElementById("newPasswordInput").value = emp.pass || "1234";

            const modal = new bootstrap.Modal(document.getElementById('changePasswordModal'));
            modal.show();
        }

        function saveNewPassword() {
            const empId = document.getElementById("resetPassEmpId").value;
            const newPass = document.getElementById("newPasswordInput").value.trim();

            if (!newPass) {
                alert("กรุณาระบุรหัสผ่านใหม่");
                return;
            }

            let employees = getEmployees();
            if (employees[empId]) {
                employees[empId].pass = newPass;
                saveEmployees(employees);
                bootstrap.Modal.getInstance(document.getElementById('changePasswordModal')).hide();
                alert("เปลี่ยนรหัสผ่านสำเร็จเรียบร้อยแล้ว");
                renderApproverView(getSession().apprId);
            }
        }

        function deleteEmployee(empId) {
            const employees = getEmployees();
            const emp = employees[empId];
            if (!emp) return;

            if (!confirm(`คุณต้องการลบพนักงาน "${emp.name}" ออกจากระบบใช่หรือไม่?\n(คำเตือน: ประวัติการลาของพนักงานรายนี้จะถูกลบออกด้วย)`)) return;

            delete employees[empId];
            saveEmployees(employees);

            let requests = getRequests().filter(r => r.empId !== empId);
            saveRequests(requests);

            alert("ลบข้อมูลพนักงานเรียบร้อยแล้ว");
            renderApproverView(getSession().apprId);
        }

        function toggleReasonField() {
            const leaveType = document.getElementById("leaveType").value;
            const leaveReason = document.getElementById("leaveReason");
            leaveReason.placeholder = `ระบุรายละเอียด/เหตุผลสำหรับการขอ "${leaveType || 'ลางาน'}"...`;
        }

        function calculateDays() {
            const isHalf = document.getElementById("modeHalf").checked;
            const startVal = document.getElementById("startDate").value;
            const endVal = document.getElementById("endDate").value;
            const textElem = document.getElementById("calculatedDaysText");
            const session = getSession();

            if (isHalf) {
                if (startVal) {
                    textElem.innerText = `0.5 วัน (ลาครึ่งวัน)`;
                    textElem.className = "fw-bold fs-4 text-primary";
                    return 0.5;
                } else {
                    textElem.innerText = "0 วัน";
                    textElem.className = "fw-bold fs-4 text-primary";
                    return 0;
                }
            }

            if (startVal && endVal) {
                let start = new Date(startVal);
                let end = new Date(endVal);

                if (end >= start) {
                    let validDaysCount = 0;
                    let curDate = new Date(start);

                    const employees = getEmployees();
                    const currentEmp = session ? employees[session.empId] : null;
                    const cId = currentEmp ? currentEmp.companyId : "COMP01";
                    
                    const companyHolidays = getHolidays().filter(h => h.companyId === cId).map(h => h.date);

                    while (curDate <= end) {
                        const dayOfWeek = curDate.getDay();
                        const y = curDate.getFullYear();
                        const m = String(curDate.getMonth() + 1).padStart(2, '0');
                        const d = String(curDate.getDate()).padStart(2, '0');
                        const dateStr = `${y}-${m}-${d}`;

                        const isSunday = (dayOfWeek === 0);
                        const isHoliday = companyHolidays.includes(dateStr);

                        if (!isSunday && !isHoliday) {
                            validDaysCount++;
                        }
                        curDate.setDate(curDate.getDate() + 1);
                    }

                    textElem.innerText = `${validDaysCount} วัน`;
                    textElem.className = "fw-bold fs-4 text-primary";
                    return validDaysCount;
                } else {
                    textElem.innerText = "วันที่สิ้นสุดต้องไม่น้อยกว่าวันที่เริ่มต้น!";
                    textElem.className = "fw-bold fs-6 text-danger";
                    return 0;
                }
            } else {
                textElem.innerText = "0 วัน";
                textElem.className = "fw-bold fs-4 text-primary";
                return 0;
            }
        }

        function handleLeaveSubmit(e) {
            e.preventDefault();
            const session = getSession();
            const employees = getEmployees();
            const companies = getCompanies();
            const currentEmp = employees[session.empId];

            const isHalf = document.getElementById("modeHalf").checked;
            const halfSession = isHalf ? document.getElementById("halfDaySession").value : null;

            const totalDays = calculateDays();
            if (totalDays <= 0) {
                alert("จำนวนวันลาจริงเป็น 0 วัน (เนื่องจากตรงกับวันหยุดนักขัตฤกษ์หรือวันอาทิตย์)");
                return;
            }

            const leaveType = document.getElementById("leaveType").value;
            const leaveReason = document.getElementById("leaveReason").value;
            const startDate = document.getElementById("startDate").value;
            const endDate = isHalf ? startDate : document.getElementById("endDate").value;
            const fileInput = document.getElementById("leaveFile");

            const handoverColleague = document.getElementById("handoverColleague").value;
            const handoverNotes = document.getElementById("handoverNotes").value.trim();

            const existingRequests = getRequests().filter(r => r.empId === currentEmp.id && (r.status === "Pending" || r.status === "Approved" || r.status === "Cancel_Pending"));
            let hasOverlap = false;
            for (let req of existingRequests) {
                if (!(endDate < req.startDate || startDate > req.endDate)) {
                    hasOverlap = true;
                    break;
                }
            }
            if (hasOverlap) {
                alert("❌ ไม่สามารถยื่นคำขอได้ เนื่องจากช่วงวันที่ท่านเลือกมีการลางานซ้ำซ้อนกับคำขออื่นในระบบ");
                return;
            }

            if (!currentEmp.quotas[leaveType]) {
                const leaveTypes = getLeaveTypes();
                currentEmp.quotas[leaveType] = { total: leaveTypes[leaveType]?.defaultQuota || 10, used: 0 };
            }
            const qInfo = currentEmp.quotas[leaveType];
            const remaining = qInfo.total - qInfo.used;

            if (totalDays > remaining) {
                if (!confirm(`คำเตือน: จำนวนวันที่ขอลา (${totalDays} วัน) เกินโควตาคงเหลือ (${remaining} วัน) คุณต้องการส่งคำขอต่อหรือไม่?`)) {
                    return;
                }
            }

            let deptEmployeesCount = 0;
            for (let eId in employees) {
                if (employees[eId].companyId === currentEmp.companyId && employees[eId].dept === currentEmp.dept) {
                    deptEmployeesCount++;
                }
            }

            let overlappingColleagues = new Set();
            const allCompanyRequests = getRequests().filter(r => r.companyId === currentEmp.companyId && r.empId !== currentEmp.id && (r.status === "Pending" || r.status === "Approved"));
            
            allCompanyRequests.forEach(r => {
                const targetEmp = employees[r.empId];
                if (targetEmp && targetEmp.dept === currentEmp.dept) {
                    if (!(endDate < r.startDate || startDate > r.endDate)) {
                        overlappingColleagues.add(r.empName);
                    }
                }
            });

            const overlappingCount = overlappingColleagues.size;
            const capacityThreshold = deptEmployeesCount > 0 ? (deptEmployeesCount / 2) : 1;

            const proceedWithFileAndSave = (fileDataUrl, fileName) => {
                pendingLeavePayload = {
                    companyId: currentEmp.companyId,
                    companyName: companies[currentEmp.companyId],
                    empId: currentEmp.id,
                    empName: currentEmp.name,
                    empDept: currentEmp.dept,
                    empEmail: currentEmp.email || (currentEmp.id.toLowerCase() + "@company.co.th"),
                    type: leaveType,
                    isHalf: isHalf,
                    halfSession: halfSession,
                    reason: leaveReason || "ไม่ได้ระบุ",
                    startDate: startDate,
                    endDate: endDate,
                    totalDays: totalDays,
                    handoverColleague: handoverColleague !== "-" ? handoverColleague : "ไม่มีการมอบหมาย",
                    handoverNotes: handoverNotes || "ไม่มีรายละเอียดงานค้าง",
                    fileName: fileName,
                    fileData: fileDataUrl
                };

                if (deptEmployeesCount > 1 && overlappingCount >= capacityThreshold) {
                    let namesList = Array.from(overlappingColleagues).join(", ");
                    document.getElementById("warningDetailList").innerHTML = `
                        <strong>แผนก:</strong> ${currentEmp.dept} (มีบุคลากรทั้งหมด ${deptEmployeesCount} คน)<br>
                        <strong>พนักงานที่ลาในช่วงเวลานี้แล้ว (${overlappingCount} คน):</strong> ${namesList}<br>
                        <span class="text-danger fw-bold">คำเตือน: มีพนักงานในแผนกเดียวกันลาในช่วงเวลานี้จำนวนมาก อาจส่งผลกระทบต่อการปฏิบัติงาน</span>
                    `;
                    const warningModal = new bootstrap.Modal(document.getElementById('smartWarningModal'));
                    warningModal.show();
                } else {
                    executeFinalLeaveSubmit(pendingLeavePayload);
                }
            };

            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                const reader = new FileReader();
                reader.onload = function(evt) {
                    proceedWithFileAndSave(evt.target.result, file.name);
                };
                reader.readAsDataURL(file);
            } else {
                proceedWithFileAndSave(null, "ไม่มีไฟล์แนบ");
            }
        }

        function confirmForceSubmitLeave() {
            const warningModalEl = document.getElementById('smartWarningModal');
            bootstrap.Modal.getInstance(warningModalEl).hide();
            if (pendingLeavePayload) {
                executeFinalLeaveSubmit(pendingLeavePayload);
            }
        }

        function executeFinalLeaveSubmit(payload) {
            const newRequest = {
                id: "LV-" + Date.now().toString().slice(-5),
                ...payload,
                createdAt: new Date().toLocaleDateString("th-TH"),
                status: "Pending",
                approvedBy: "-",
                rejectionReason: "",
                cancelReason: ""
            };

            const requests = getRequests();
            requests.unshift(newRequest);
            saveRequests(requests);

            document.getElementById("leaveForm").reset();
            document.getElementById("modeFull").checked = true;
            onDurationModeChange();
            document.getElementById("calculatedDaysText").innerText = "0 วัน";
            
            if (payload.handoverColleague !== "ไม่มีการมอบหมาย") {
                alert(`🔔 ส่งคำขอลางานสำเร็จ!\nระบบได้ส่งการแจ้งเตือนงานมอบหมายไปยัง "${payload.handoverColleague}" เรียบร้อยแล้ว`);
            } else {
                alert(`🔔 ส่งคำขอลางานสำเร็จ! ระบบได้ส่ง Notification แจ้งเตือนไปยังผู้อนุมัติเรียบร้อยแล้ว`);
            }

            pendingLeavePayload = null;
            renderEmployeeView(getSession().empId);
        }

        function handleCancelRequest(requestId) {
            if (!confirm("คุณต้องการยกเลิกคำขอลางานนี้ใช่หรือไม่?")) return;

            let requests = getRequests();
            const reqIndex = requests.findIndex(r => r.id === requestId);

            if (reqIndex !== -1) {
                if (requests[reqIndex].status !== "Pending") {
                    alert("ไม่สามารถยกเลิกคำขอนี้ได้โดยตรง");
                    return;
                }

                requests[reqIndex].status = "Cancelled";
                requests[reqIndex].approvedBy = "ยกเลิกโดยพนักงานเอง";
                saveRequests(requests);

                alert("ยกเลิกคำขอลางานเรียบร้อยแล้ว");
                renderEmployeeView(getSession().empId);
            }
        }

        function openEmployeeCancelModal(requestId) {
            document.getElementById("cancelRequestIdInput").value = requestId;
            document.getElementById("employeeCancelReasonText").value = "";
            const modal = new bootstrap.Modal(document.getElementById('employeeCancelReasonModal'));
            modal.show();
        }

        function submitEmployeeCancelRequest() {
            const reqId = document.getElementById("cancelRequestIdInput").value;
            const reason = document.getElementById("employeeCancelReasonText").value.trim();

            if (!reason) {
                alert("กรุณาระบุเหตุผลในการขอยกเลิก/คืนวันลา");
                return;
            }

            let requests = getRequests();
            const reqIndex = requests.findIndex(r => r.id === reqId);

            if (reqIndex !== -1) {
                requests[reqIndex].status = "Cancel_Pending";
                requests[reqIndex].cancelReason = reason;
                saveRequests(requests);

                bootstrap.Modal.getInstance(document.getElementById('employeeCancelReasonModal')).hide();
                alert("🔔 ส่งคำขอคืนวันลาไปยังผู้อนุมัติสำเร็จแล้ว รอการตรวจสอบและคืนโควตา");
                renderEmployeeView(getSession().empId);
            }
        }

        function renderEmployeeHistory(empId) {
            const requests = getRequests().filter(r => r.empId === empId);
            const tbody = document.getElementById("employeeHistoryTable");
            tbody.innerHTML = "";

            if (requests.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">ไม่พบบันทึกการลางาน</td></tr>`;
                return;
            }

            requests.forEach(req => {
                let badgeClass = "bg-warning text-dark";
                let statusTh = "รออนุมัติ";
                if (req.status === "Approved") { badgeClass = "bg-success"; statusTh = "อนุมัติแล้ว"; }
                else if (req.status === "Rejected") { badgeClass = "bg-danger"; statusTh = "ไม่อนุมัติ"; }
                else if (req.status === "Cancelled") { badgeClass = "bg-secondary"; statusTh = "ยกเลิกแล้ว"; }
                else if (req.status === "Cancel_Pending") { badgeClass = "bg-info text-dark"; statusTh = "รออนุมัติคืนวันลา"; }

                let actionBtn = "";
                if (req.status === "Pending") {
                    actionBtn = `<button class="btn btn-outline-danger btn-sm px-2 py-1" onclick="handleCancelRequest('${req.id}')"><i class="bi bi-x-circle me-1"></i> ยกเลิก</button>`;
                } else if (req.status === "Approved") {
                    actionBtn = `<button class="btn btn-outline-warning btn-sm px-2 py-1 text-dark fw-bold" onclick="openEmployeeCancelModal('${req.id}')"><i class="bi bi-arrow-counterclockwise me-1"></i> ขอคืนวันลา</button>`;
                } else if (req.status === "Cancel_Pending") {
                    actionBtn = `<span class="badge bg-light text-dark border">รอพิจารณา</span>`;
                } else {
                    actionBtn = `<span class="text-muted small">${statusTh}</span>`;
                }

                let rejectionInfo = "";
                if (req.status === "Rejected" && req.rejectionReason) {
                    rejectionInfo = `<div class="text-danger small mt-1"><strong>เหตุผลที่ไม่อนุมัติ:</strong> ${req.rejectionReason}</div>`;
                }
                if (req.status === "Cancel_Pending" && req.cancelReason) {
                    rejectionInfo = `<div class="text-info small mt-1"><strong>เหตุผลขอคืน:</strong> ${req.cancelReason}</div>`;
                }

                let typeDisplay = req.type;
                if (req.isHalf) {
                    let sText = req.halfSession === 'morning' ? 'ครึ่งวันเช้า' : 'ครึ่งวันบ่าย';
                    typeDisplay += ` <br><span class="badge bg-light text-primary border">${sText}</span>`;
                }

                let handoverDisplay = req.handoverColleague && req.handoverColleague !== "ไม่มีการมอบหมาย" ? 
                    `<small class="text-primary"><i class="bi bi-person-check"></i> ${req.handoverColleague}</small>` : 
                    `<small class="text-muted">-</small>`;

                tbody.innerHTML += `
                    <tr>
                        <td><small class="text-muted">${req.createdAt}</small></td>
                        <td><span class="fw-bold">${typeDisplay}</span></td>
                        <td><small>${req.startDate}${req.startDate !== req.endDate ? '<br>ถึง ' + req.endDate : ''}</small></td>
                        <td>${handoverDisplay}</td>
                        <td>
                            <span class="badge ${badgeClass} status-badge">${statusTh}</span>
                            ${rejectionInfo}
                        </td>
                        <td class="text-center">${actionBtn}</td>
                    </tr>
                `;
            });
        }

        function renderApproverTable(approverCompanyId) {
            let requests = getRequests().filter(r => r.companyId === approverCompanyId);
            
            let pendingRequests = requests.filter(r => r.status === "Pending" || r.status === "Cancel_Pending");
            let pendingCount = pendingRequests.length;

            const banner = document.getElementById("approverNotificationBanner");
            const countBadgeTop = document.getElementById("pendingNotificationCount");
            const countBadgeTable = document.getElementById("pendingBadgeCount");

            if (pendingCount > 0) {
                banner.classList.remove("d-none");
                banner.classList.add("d-flex");
                countBadgeTop.innerText = pendingCount;
                countBadgeTable.innerText = `${pendingCount} รายการรอตรวจสอบ`;
                countBadgeTable.className = "badge bg-danger rounded-pill px-2 py-1 me-2 shadow-sm";
            } else {
                banner.classList.remove("d-flex");
                banner.classList.add("d-none");
                countBadgeTable.innerText = "ไม่มีรายการรอตรวจสอบ";
                countBadgeTable.className = "badge bg-secondary rounded-pill px-2 py-1 me-2";
            }

            const tbody = document.getElementById("approverTable");
            tbody.innerHTML = "";

            if (requests.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted py-4">ยังไม่มีคำขอลางานในบริษัทนี้</td></tr>`;
                return;
            }

            requests.forEach(req => {
                let badgeClass = "bg-warning text-dark";
                let statusTh = "รออนุมัติ";
                if (req.status === "Approved") { badgeClass = "bg-success"; statusTh = "อนุมัติแล้ว"; }
                else if (req.status === "Rejected") { badgeClass = "bg-danger"; statusTh = "ไม่อนุมัติ"; }
                else if (req.status === "Cancelled") { badgeClass = "bg-secondary"; statusTh = "ยกเลิกแล้ว"; }
                else if (req.status === "Cancel_Pending") { badgeClass = "bg-info text-dark"; statusTh = "ขอยกเลิก/คืนวันลา"; }

                let extraInfo = "";
                if (req.status === "Rejected" && req.rejectionReason) {
                    extraInfo = `<br><small class="text-danger">เหตุผล: ${req.rejectionReason}</small>`;
                } else if (req.status === "Cancel_Pending" && req.cancelReason) {
                    extraInfo = `<br><small class="text-info fw-bold">เหตุผลขอคืน: ${req.cancelReason}</small>`;
                }

                let typeDisplay = req.type;
                if (req.isHalf) {
                    let sText = req.halfSession === 'morning' ? 'ครึ่งวันเช้า' : 'ครึ่งวันบ่าย';
                    typeDisplay += ` <br><span class="badge bg-light text-primary border">${sText}</span>`;
                }

                let handoverDisplay = req.handoverColleague && req.handoverColleague !== "ไม่มีการมอบหมาย" ? 
                    `<small class="text-primary fw-bold"><i class="bi bi-person-check"></i> ${req.handoverColleague}</small>` : 
                    `<small class="text-muted">-</small>`;

                let rowHighlight = (req.status === 'Pending' || req.status === 'Cancel_Pending') ? 'table-warning' : '';

                tbody.innerHTML += `
                    <tr class="${rowHighlight}">
                        <td><strong>${req.id}</strong></td>
                        <td><small class="badge bg-secondary">${req.companyName || 'N/A'}</small></td>
                        <td>${req.empName} <br><small class="text-muted">${req.empDept}</small></td>
                        <td>${typeDisplay}</td>
                        <td><small>${req.startDate}${req.startDate !== req.endDate ? ' ถึง <br>' + req.endDate : ''}</small></td>
                        <td>${handoverDisplay}</td>
                        <td><span class="badge ${badgeClass} status-badge">${statusTh}</span>${extraInfo}</td>
                        <td class="text-center">
                            ${(req.status === 'Pending' || req.status === 'Cancel_Pending') ? `<button class="btn btn-sm btn-primary fw-bold px-3 py-1 shadow-sm" onclick="openDetailModal('${req.id}')"><i class="bi bi-eye-fill me-1"></i> ตรวจสอบ</button>` : `<span class="text-muted small">${statusTh}</span>`}
                        </td>
                    </tr>
                `;
            });
        }

        function scrollToPendingTable() {
            document.getElementById("pendingRequestsCard").scrollIntoView({ behavior: 'smooth' });
        }

        function openEditQuotaModal(empId) {
            const employees = getEmployees();
            const leaveTypes = getLeaveTypes();
            const emp = employees[empId];
            if (!emp) return;

            document.getElementById("editQuotaEmpId").value = empId;
            document.getElementById("editQuotaEmpName").innerText = `${emp.name} (${emp.dept})`;

            const container = document.getElementById("editQuotaFieldsContainer");
            container.innerHTML = "";

            for (let lKey in leaveTypes) {
                if (!emp.quotas[lKey]) {
                    emp.quotas[lKey] = { total: leaveTypes[lKey].defaultQuota, used: 0 };
                }
                const q = emp.quotas[lKey];
                container.innerHTML += `
                    <div class="row align-items-center">
                        <div class="col-6">
                            <label class="form-label fw-bold mb-0">${lKey}:</label>
                            <small class="text-muted d-block">ใช้ไปแล้ว ${q.used} วัน</small>
                        </div>
                        <div class="col-6">
                            <input type="number" step="0.5" class="form-control quota-input-field" data-leavetype="${lKey}" value="${q.total}" min="0">
                        </div>
                    </div>
                `;
            }

            const modal = new bootstrap.Modal(document.getElementById('editQuotaModal'));
            modal.show();
        }

        function saveEmployeeQuotaChanges() {
            const empId = document.getElementById("editQuotaEmpId").value;
            const employees = getEmployees();
            const emp = employees[empId];
            if (!emp) return;

            const inputs = document.querySelectorAll(".quota-input-field");
            inputs.forEach(input => {
                const lType = input.getAttribute("data-leavetype");
                const newTotal = parseFloat(input.value) || 0;
                if (!emp.quotas[lType]) {
                    emp.quotas[lType] = { total: newTotal, used: 0 };
                } else {
                    emp.quotas[lType].total = newTotal;
                }
            });

            saveEmployees(employees);
            bootstrap.Modal.getInstance(document.getElementById('editQuotaModal')).hide();
            alert("อัปเดตโควตาวันลาพนักงานเรียบร้อยแล้ว");
            renderApproverView(getSession().apprId);
        }

        function openLeaveTypeConfigModal() {
            renderLeaveTypesConfigTable();
            const modal = new bootstrap.Modal(document.getElementById('leaveTypeConfigModal'));
            modal.show();
        }

        function renderLeaveTypesConfigTable() {
            const leaveTypes = getLeaveTypes();
            const tbody = document.getElementById("leaveTypesConfigTable");
            tbody.innerHTML = "";

            for (let lKey in leaveTypes) {
                const lt = leaveTypes[lKey];
                const isDefault = ["ลาพักร้อน", "ลาป่วย", "ลากิจ"].includes(lKey);
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${lt.name}</strong></td>
                        <td class="text-center"><span class="badge bg-info text-dark">${lt.defaultQuota} วัน</span></td>
                        <td class="text-center">
                            ${!isDefault ? `<button class="btn btn-sm btn-outline-danger px-2 py-1" onclick="deleteLeaveType('${lKey}')"><i class="bi bi-trash"></i> ลบ</button>` : `<small class="text-muted">ระบบหลัก</small>`}
                        </td>
                    </tr>
                `;
            }
        }

        function addNewLeaveType() {
            const nameInput = document.getElementById("newLeaveTypeName");
            const quotaInput = document.getElementById("newLeaveTypeDefaultQuota");

            const name = nameInput.value.trim();
            const defaultQuota = parseFloat(quotaInput.value);

            if (!name) {
                alert("กรุณาระบุชื่อประเภทการลา");
                return;
            }

            let leaveTypes = getLeaveTypes();
            if (leaveTypes[name]) {
                alert("มีประเภทการลานี้อยู่แล้วในระบบ");
                return;
            }

            leaveTypes[name] = { name: name, defaultQuota: defaultQuota || 10, color: "text-secondary" };
            saveLeaveTypes(leaveTypes);

            let employees = getEmployees();
            for (let eId in employees) {
                if (!employees[eId].quotas[name]) {
                    employees[eId].quotas[name] = { total: defaultQuota || 10, used: 0 };
                }
            }
            saveEmployees(employees);

            nameInput.value = "";
            quotaInput.value = "10";
            renderLeaveTypesConfigTable();
            alert(`เพิ่มประเภทการลา "${name}" สำเร็จ`);
            renderApproverView(getSession().apprId);
        }

        function deleteLeaveType(lKey) {
            if (!confirm(`คุณต้องการลบประเภทการลา "${lKey}" ใช่หรือไม่?`)) return;

            let leaveTypes = getLeaveTypes();
            delete leaveTypes[lKey];
            saveLeaveTypes(leaveTypes);

            renderLeaveTypesConfigTable();
            alert("ลบประเภทการลาเรียบร้อยแล้ว");
            renderApproverView(getSession().apprId);
        }

        function openDetailModal(requestId) {
            activeLeaveIdForApproval = requestId;
            const req = getRequests().find(r => r.id === requestId);
            if (!req) return;

            const modalTitleElem = document.getElementById("detailModalTitle");
            const footerElem = document.getElementById("detailModalFooter");
            const cancelReasonBox = document.getElementById("modalCancelReasonBox");

            document.getElementById("modalCompName").innerText = req.companyName || '-';
            document.getElementById("modalEmpName").innerText = req.empName;
            document.getElementById("modalEmpId").innerText = req.empId;
            document.getElementById("modalEmpDept").innerText = req.empDept;
            
            let typeStr = req.type;
            if (req.isHalf) {
                typeStr += req.halfSession === 'morning' ? ' (ครึ่งวันเช้า)' : ' (ครึ่งวันบ่าย)';
            }
            document.getElementById("modalLeaveType").innerText = typeStr;
            document.getElementById("modalStartDate").innerText = req.startDate;
            document.getElementById("modalEndDate").innerText = req.endDate;
            document.getElementById("modalTotalDays").innerText = `${req.totalDays} วัน`;
            document.getElementById("modalReason").innerText = req.reason;

            document.getElementById("modalHandover").innerText = req.handoverColleague || "ไม่มีการมอบหมาย";
            document.getElementById("modalHandoverNotesBox").innerHTML = req.handoverNotes ? `<strong>โน้ต/งานค้าง:</strong> ${req.handoverNotes}` : "";

            if (req.status === "Cancel_Pending") {
                modalTitleElem.innerHTML = `<i class="bi bi-arrow-counterclockwise me-2"></i> คำขออนุมัติคืนวันลา (Cancellation Request)`;
                cancelReasonBox.classList.remove("d-none");
                document.getElementById("modalCancelReason").innerText = req.cancelReason || "ไม่มีระบุ";
                
                footerElem.innerHTML = `
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ปิด</button>
                    <button type="button" class="btn btn-danger px-4" onclick="processCancelApproval('Reject_Cancel')">ปฏิเสธคำขอคืน</button>
                    <button type="button" class="btn btn-success px-4" onclick="processCancelApproval('Approve_Cancel')"><i class="bi bi-check-circle me-1"></i> อนุมัติคืนวันลา (คืนโควตา)</button>
                `;
            } else {
                modalTitleElem.innerHTML = `<i class="bi bi-person-vcard me-2"></i> รายละเอียดคำขอลางาน`;
                cancelReasonBox.classList.add("d-none");

                footerElem.innerHTML = `
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ปิดหน้าต่าง</button>
                    <button type="button" class="btn btn-danger px-4" onclick="promptRejectReason()">
                        <i class="bi bi-x-circle me-1"></i> Reject (ไม่อนุมัติ)
                    </button>
                    <button type="button" class="btn btn-success px-4" onclick="processApproval('Approved')">
                        <i class="bi bi-check-circle me-1"></i> Approve (อนุมัติ)
                    </button>
                `;
            }

            const modalFileElem = document.getElementById("modalFile");
            currentActiveFileData = req.fileData;
            currentActiveFileName = req.fileName;

            if (req.fileData && req.fileName !== "ไม่มีไฟล์แนบ") {
                modalFileElem.innerHTML = `
                    <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                        <span class="small text-truncate" style="max-width: 220px;" title="${req.fileName}"><i class="bi bi-file-earmark-text me-1 text-primary"></i>${req.fileName}</span>
                        <div class="d-flex gap-1">
                            <button type="button" class="btn btn-sm btn-info text-white fw-bold" onclick="openDocPreviewModal()">
                                <i class="bi bi-eye me-1"></i> ดูตัวอย่าง
                            </button>
                            <a href="${req.fileData}" download="${req.fileName}" class="btn btn-sm btn-outline-primary" title="ดาวน์โหลด">
                                <i class="bi bi-download"></i>
                            </a>
                        </div>
                    </div>
                `;
            } else {
                modalFileElem.innerHTML = `<span class="text-muted small">ไม่มีไฟล์แนบ</span>`;
            }

            const modal = new bootstrap.Modal(document.getElementById('detailModal'));
            modal.show();
        }

        function openDocPreviewModal() {
            if (!currentActiveFileData) return;

            const detailModalEl = document.getElementById('detailModal');
            const detailModalInstance = bootstrap.Modal.getInstance(detailModalEl);
            if (detailModalInstance) detailModalInstance.hide();

            document.getElementById("previewFileName").innerText = currentActiveFileName;
            document.getElementById("previewDownloadBtn").href = currentActiveFileData;
            document.getElementById("previewDownloadBtn").setAttribute("download", currentActiveFileName);

            const container = document.getElementById("previewContainer");
            container.innerHTML = "";

            if (currentActiveFileData.startsWith("data:image/") || currentActiveFileName.match(/\.(jpg|jpeg|png|gif|webp)$/i)) {
                container.innerHTML = `<img src="${currentActiveFileData}" alt="${currentActiveFileName}" class="img-fluid rounded shadow" style="max-height: 70vh; object-fit: contain;">`;
            } else if (currentActiveFileData.startsWith("data:application/pdf") || currentActiveFileName.match(/\.pdf$/i)) {
                container.innerHTML = `<iframe src="${currentActiveFileData}" type="application/pdf" width="100%" height="600px" class="rounded border bg-white shadow-sm"></iframe>`;
            } else {
                container.innerHTML = `
                    <div class="p-5 text-center">
                        <i class="bi bi-file-earmark-text display-1 text-muted mb-3"></i>
                        <p class="fw-bold">ไม่สามารถแสดงตัวอย่างไฟล์ประเภทนี้โดยตรงได้</p>
                        <a href="${currentActiveFileData}" download="${currentActiveFileName}" class="btn btn-primary mt-2">
                            <i class="bi bi-download me-1"></i> คลิกเพื่อดาวน์โหลดและเปิดดู
                        </a>
                    </div>
                `;
            }

            const previewModal = new bootstrap.Modal(document.getElementById('docPreviewModal'));
            previewModal.show();
        }

        function closePreviewModal() {
            const previewModalEl = document.getElementById('docPreviewModal');
            const previewModalInstance = bootstrap.Modal.getInstance(previewModalEl);
            if (previewModalInstance) previewModalInstance.hide();

            const detailModal = new bootstrap.Modal(document.getElementById('detailModal'));
            detailModal.show();
        }

        function promptRejectReason() {
            const detailModalEl = document.getElementById('detailModal');
            const detailModal = bootstrap.Modal.getInstance(detailModalEl);
            if (detailModal) detailModal.hide();

            document.getElementById("rejectionReasonInput").value = "";
            const reasonModal = new bootstrap.Modal(document.getElementById('rejectReasonModal'));
            reasonModal.show();
        }

        function confirmRejectWithReason() {
            const reasonText = document.getElementById("rejectionReasonInput").value.trim();
            if (!reasonText) {
                alert("กรุณาระบุเหตุผลในการไม่อนุมัติ เพื่อให้พนักงานรับทราบ");
                return;
            }

            const requests = getRequests();
            const reqIndex = requests.findIndex(r => r.id === activeLeaveIdForApproval);

            if (reqIndex !== -1) {
                const req = requests[reqIndex];
                const session = getSession();
                const approvers = getApprovers();
                
                const curAppr = approvers[session.apprId];
                let approverTitle = curAppr ? `${curAppr.name} (${curAppr.position})` : "ผู้อนุมัติ";

                requests[reqIndex].status = "Rejected";
                requests[reqIndex].rejectionReason = reasonText;
                requests[reqIndex].approvedBy = approverTitle;
                saveRequests(requests);

                const reasonModalEl = document.getElementById('rejectReasonModal');
                bootstrap.Modal.getInstance(reasonModalEl).hide();

                showEmailSimulation(req, "Rejected", approverTitle);
            }
        }

        function processApproval(newStatus) {
            const requests = getRequests();
            const reqIndex = requests.findIndex(r => r.id === activeLeaveIdForApproval);

            if (reqIndex !== -1) {
                const req = requests[reqIndex];
                const session = getSession();
                const approvers = getApprovers();
                const employees = getEmployees();

                const curAppr = approvers[session.apprId];
                let approverTitle = curAppr ? `${curAppr.name} (${curAppr.position})` : "ผู้อนุมัติ";

                if (newStatus === "Approved" && req.status !== "Approved") {
                    const emp = employees[req.empId];
                    if (emp) {
                        const days = req.totalDays;
                        if (!emp.quotas[req.type]) {
                            emp.quotas[req.type] = { total: 10, used: 0 };
                        }
                        emp.quotas[req.type].used += days;
                        saveEmployees(employees);
                    }
                }

                requests[reqIndex].status = newStatus;
                requests[reqIndex].rejectionReason = "";
                requests[reqIndex].approvedBy = approverTitle;
                saveRequests(requests);

                bootstrap.Modal.getInstance(document.getElementById('detailModal')).hide();
                
                showEmailSimulation(req, newStatus, approverTitle);
            }
        }

        function processCancelApproval(actionType) {
            const requests = getRequests();
            const reqIndex = requests.findIndex(r => r.id === activeLeaveIdForApproval);

            if (reqIndex !== -1) {
                const req = requests[reqIndex];
                const session = getSession();
                const approvers = getApprovers();
                const employees = getEmployees();

                const curAppr = approvers[session.apprId];
                let approverTitle = curAppr ? `${curAppr.name} (${curAppr.position})` : "ผู้อนุมัติ";

                if (actionType === "Approve_Cancel") {
                    const emp = employees[req.empId];
                    if (emp && emp.quotas[req.type]) {
                        emp.quotas[req.type].used = Math.max(0, emp.quotas[req.type].used - req.totalDays);
                        saveEmployees(employees);
                    }

                    requests[reqIndex].status = "Cancelled";
                    requests[reqIndex].approvedBy = `อนุมัติคืนวันลาโดย ${approverTitle}`;
                    saveRequests(requests);

                    bootstrap.Modal.getInstance(document.getElementById('detailModal')).hide();
                    showEmailSimulation(req, "Cancel_Approved", approverTitle);
                } else {
                    requests[reqIndex].status = "Approved";
                    requests[reqIndex].approvedBy = approverTitle;
                    saveRequests(requests);

                    bootstrap.Modal.getInstance(document.getElementById('detailModal')).hide();
                    alert("ปฏิเสธคำขอคืนวันลาเรียบร้อยแล้ว รายการยังคงสถานะอนุมัติเดิม");
                    renderApproverView(session.apprId);
                }
            }
        }

        function showEmailSimulation(req, status, approverName) {
            const emailTo = req.empEmail || (req.empId.toLowerCase() + "@company.co.th");
            
            let subject = "";
            let messageText = "";

            if (status === "Approved") {
                subject = `[แจ้งผลการพิจารณา] คำขอลา "${req.type}" ของคุณได้รับการอนุมัติแล้ว`;
                messageText = `คำขอลางานประเภท "${req.type}" ของท่าน (ช่วงวันที่ ${req.startDate} ถึง ${req.endDate}, จำนวน ${req.totalDays} วัน) ได้รับการอนุมัติเรียบร้อยแล้ว`;
            } else if (status === "Rejected") {
                subject = `[แจ้งผลการพิจารณา] คำขอลา "${req.type}" ของคุณไม่ได้รับการอนุมัติ`;
                messageText = `คำขอลางานประเภท "${req.type}" ของท่าน ไม่ได้รับการอนุมัติ เนื่องจาก: "${req.rejectionReason || 'ติดภาระกิจงานด่วน'}"`;
            } else if (status === "Cancel_Approved") {
                subject = `[แจ้งผลการคืนวันลา] คำขอยกเลิกและคืนวันลา "${req.type}" สำเร็จแล้ว`;
                messageText = `ระบบได้ทำการยกเลิกวันลาและ **คืนโควตาวันลาจำนวน ${req.totalDays} วัน** กลับสู่บัญชีของท่านเรียบร้อยแล้วครับ`;
            }
            
            document.getElementById("simEmailTo").innerText = emailTo;
            document.getElementById("simEmailSubject").innerText = subject;
            document.getElementById("simEmpName").innerText = req.empName;
            document.getElementById("simEmailMessage").innerText = messageText;
            document.getElementById("simLeaveDetails").innerText = `${req.type} (${req.totalDays} วัน | ${req.startDate} ถึง ${req.endDate})`;
            document.getElementById("simApproverName").innerText = approverName;

            const emailModal = new bootstrap.Modal(document.getElementById('emailSimulationModal'));
            emailModal.show();

            const emailModalEl = document.getElementById('emailSimulationModal');
            emailModalEl.addEventListener('hidden.bs.modal', function () {
                const session = getSession();
                if (session && session.role === "approver") {
                    renderApproverView(session.apprId);
                }
            }, { once: true });
        }

        function openResetModal() {
            const modal = new bootstrap.Modal(document.getElementById('resetModal'));
            modal.show();
        }

        function confirmResetQuota() {
            const employees = getEmployees();
            for (let id in employees) {
                for (let lKey in employees[id].quotas) {
                    employees[id].quotas[lKey].used = 0;
                }
            }
            saveEmployees(employees);
            saveRequests([]);
            bootstrap.Modal.getInstance(document.getElementById('resetModal')).hide();
            alert("รีเซ็ตสิทธิวันลาเรียบร้อยแล้ว");
            location.reload();
        }

        window.onload = initData;
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    print("กำลังเริ่มทำงานระบบ Leave Management System (แก้ไขฟังก์ชันเพิ่มบริษัทเรียบร้อยแล้ว)...")
    print("เปิดเบราว์เซอร์ไปที่: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)