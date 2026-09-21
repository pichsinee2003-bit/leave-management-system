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
    </style>
</head>
<body>

    <!-- ==================== 1. PAGE: LOGIN VIEW ==================== -->
    <div id="loginView" class="d-flex align-items-center justify-content-center min-vh-100 py-4">
        <div class="login-container px-3">
            <div class="text-center mb-4">
                <i class="bi bi-building-gear text-primary display-3"></i>
                <h3 class="fw-bold mt-2">ระบบบริหารจัดการการลางาน</h3>
                <p class="text-muted small">กรุณาเข้าสู่ระบบเพื่อใช้งาน (รองรับ 5 บริษัทกลุ่ม)</p>
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
                            <i class="bi bi-shield-lock me-1"></i> ผู้อนุมัติ / HR Admin
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
                            <div class="mb-3">
                                <label class="form-label fw-bold small"><i class="bi bi-building me-1"></i> เลือกบริษัท:</label>
                                <select id="loginApprCompanySelect" class="form-select" onchange="onLoginApprCompanyChange(this.value)">
                                    <!-- Dynamic -->
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold small"><i class="bi bi-person-badge me-1"></i> เลือกผู้อนุมัติ / HR:</label>
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
                                <!-- Live Overlap & Capacity Warning Box -->
                                <div id="liveOverlapWarning" class="alert alert-warning d-none shadow-sm mb-3" role="alert">
                                    <div class="d-flex">
                                        <i class="bi bi-exclamation-triangle-fill fs-4 me-2 text-warning flex-shrink-0"></i>
                                        <div>
                                            <strong>คำเตือน (Smart Warning):</strong> 
                                            <span id="overlapWarningText">มีพนักงานในแผนกเดียวกันลาในช่วงเวลานี้จำนวนมาก เกิน 50% อาจส่งผลกระทบต่อการปฏิบัติงาน</span>
                                        </div>
                                    </div>
                                </div>

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
                                                <label class="form-check-label fw-semibold" for="modeHalf">
                                                    ครึ่งวัน (Half-Day)
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

                                    <div class="mb-3 p-3 bg-light rounded border text-center">
                                        <div class="fw-bold text-secondary">จำนวนวันลาครั้งนี้:</div>
                                        <span id="calculatedDaysText" class="fw-bold fs-4 text-primary">0 วัน</span>
                                        <div class="text-muted small mt-1"><i class="bi bi-info-circle me-1"></i>ระบบยกเว้นวันอาทิตย์และวันหยุดนักขัตฤกษ์ให้อัตโนมัติ</div>
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
                                <small class="text-white-50"><i class="bi bi-info-circle me-1"></i> ยกเลิกได้เฉพาะสถานะ "รออนุมัติ"</small>
                            </div>
                            <div class="card-body p-0">
                                <div class="table-responsive">
                                    <table class="table table-hover align-middle mb-0">
                                        <thead class="table-light">
                                            <tr>
                                                <th>วันที่ยื่น</th>
                                                <th>ประเภท</th>
                                                <th>ช่วงวันที่ลา</th>
                                                <th>จำนวนวัน</th>
                                                <th>สถานะ</th>
                                                <th>ผู้อนุมัติ</th>
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
                <!-- Delegate Alert Banner -->
                <div id="delegateAlertBanner" class="alert alert-warning shadow-sm mb-3 d-none align-items-center justify-content-between">
                    <div>
                        <i class="bi bi-shield-exclamation fs-4 me-2"></i>
                        <strong>แจ้งเตือนสถานะผู้รักษาการแทน:</strong> มีการตั้งค่ามอบหมายสิทธิ์ให้ <span id="delegateActiveName" class="fw-bold text-dark">-</span> ปฏิบัติหน้าที่แทน (ตั้งแต่ <span id="delegateStartText"></span> ถึง <span id="delegateEndText"></span>)
                    </div>
                </div>

                <div class="alert alert-info d-flex align-items-center justify-content-between shadow-sm mb-4 flex-wrap gap-2">
                    <div class="d-flex align-items-center gap-3">
                        <i class="bi bi-shield-check fs-3"></i>
                        <div>
                            <strong>โหมดผู้บริหาร / HR Admin:</strong> ท่านกำลังจัดการระบบของ
                            <span id="approverCompanyText" class="badge bg-primary fs-6 ms-1">-</span>
                        </div>
                    </div>
                    <div class="d-flex gap-2 flex-wrap">
                        <button class="btn btn-outline-dark btn-sm fw-bold bg-white" onclick="openDelegateModal()">
                            <i class="bi bi-person-fill-gear me-1"></i> ตั้งค่าผู้อนุมัติสำรอง (Delegate)
                        </button>
                        <button class="btn btn-primary btn-sm fw-bold" onclick="openAddEmployeeModal()">
                            <i class="bi bi-person-plus-fill me-1"></i> เพิ่มพนักงานใหม่
                        </button>
                        <button class="btn btn-dark btn-sm fw-bold" onclick="openLeaveTypeConfigModal()">
                            <i class="bi bi-gear-fill me-1"></i> จัดการประเภทการลา
                        </button>
                        <button class="btn btn-warning btn-sm fw-bold text-dark" onclick="openResetModal()">
                            <i class="bi bi-arrow-counterclockwise me-1"></i> รีเซ็ตวันลา
                        </button>
                    </div>
                </div>

                <!-- NOTIFICATION ALERT BANNER FOR APPROVER -->
                <div id="approverNotificationBanner" class="alert alert-danger shadow-sm mb-4 d-none align-items-center justify-content-between">
                    <div class="d-flex align-items-center gap-2">
                        <i class="bi bi-bell-fill fs-4 animate-bounce"></i>
                        <div>
                            <strong>🔔 แจ้งเตือนคำขอใหม่:</strong> มีคำขอลางานใหม่จำนวน <span id="pendingNotificationCount" class="badge bg-white text-danger fw-bold fs-6">0</span> รายการ ที่รอการตรวจสอบและอนุมัติจากท่าน
                        </div>
                    </div>
                    <button class="btn btn-sm btn-light text-danger fw-bold shadow-sm" onclick="scrollToPendingTable()">
                        ตรวจสอบทันที
                    </button>
                </div>

                <!-- TEAM LEAVE CALENDAR VIEW -->
                <div class="card mb-4">
                    <div class="card-header bg-primary py-3 d-flex justify-content-between align-items-center flex-wrap gap-2">
                        <span><i class="bi bi-calendar-check-fill me-2"></i> ปฏิทินวันลาของทีม (Team Calendar View)</span>
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
                    <div class="mt-2 text-muted small d-flex gap-3 align-items-center">
                        <span><i class="bi bi-circle-fill text-primary" style="font-size: 0.6rem;"></i> <strong>สีฟ้า:</strong> ลาพักร้อน</span>
                        <span><i class="bi bi-circle-fill text-success" style="font-size: 0.6rem;"></i> <strong>สีเขียว:</strong> ลาป่วย</span>
                        <span><i class="bi bi-circle-fill text-warning" style="font-size: 0.6rem;"></i> <strong>สีเหลือง/ส้ม:</strong> ลากิจหรือประเภทอื่น</span>
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
                        <span><i class="bi bi-list-check me-2"></i> รายการคำขอลางานภายในบริษัท</span>
                        <div>
                            <span id="pendingBadgeCount" class="badge bg-danger rounded-pill px-2 py-1 me-2 shadow-sm" style="font-size: 0.85rem;">0 รายการรออนุมัติ</span>
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
                                        <th>จำนวนวัน</th>
                                        <th>สถานะปัจจุบัน</th>
                                        <th>ผู้อนุมัติ</th>
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

    <!-- MODAL 1: Details & Approval Modal -->
    <div class="modal fade" id="detailModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title fw-bold">
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
                            
                            <!-- Capacity Warning Display in Modal for Approver -->
                            <div id="modalOverlapWarningBox" class="alert alert-warning p-2 mt-2 mb-2 d-none small">
                                <i class="bi bi-exclamation-triangle-fill me-1"></i> <strong>Smart Warning:</strong> มีพนักงานในแผนกเดียวกันลาเกิน 50% ในช่วงเวลานี้
                            </div>

                            <p class="mb-1 mt-2"><strong>เหตุผลประกอบ:</strong> <span id="modalReason" class="text-danger">-</span></p>
                            <div class="mb-1 mt-3 p-2 bg-light rounded border">
                                <strong>เอกสารแนบประกอบ:</strong> 
                                <div id="modalFile" class="mt-2">-</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer bg-light">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ปิดหน้าต่าง</button>
                    <button type="button" class="btn btn-danger px-4" onclick="promptRejectReason()">
                        <i class="bi bi-x-circle me-1"></i> Reject (ไม่อนุมัติ)
                    </button>
                    <button type="button" class="btn btn-success px-4" onclick="processApproval('Approved')">
                        <i class="bi bi-check-circle me-1"></i> Approve (อนุมัติ)
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Email Simulation Modal (จำลองระบบส่งอีเมลแจ้งเตือน) -->
    <div class="modal fade" id="emailSimulationModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content shadow-lg border-0">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-envelope-at-fill text-info me-2"></i>จำลองการส่งอีเมลแจ้งเตือนพนักงาน (Email Simulation)</h5>
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
                            <p class="mb-2">เรียน คุณ <span id="simEmpName" class="fw-bold">-</span>,</p>
                            <p id="simEmailMessage" class="mb-3 text-secondary p-2 bg-white rounded border">-</p>
                            <div class="small text-muted">
                                รายละเอียดคำขอ: <span id="simLeaveDetails" class="fw-bold text-dark">-</span><br>
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

    <!-- MODAL: Delegate Approver Modal -->
    <div class="modal fade" id="delegateModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title fw-bold"><i class="bi bi-person-fill-gear me-2"></i>ตั้งค่าผู้อนุมัติสำรอง (Delegate Approver)</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p class="small text-muted">ในกรณีที่ท่าน (ผู้จัดการ/ผู้อนุมัติหลัก) ลาพักร้อน สามารถเลือกพนักงานในสังกัดให้ปฏิบัติหน้าที่ผู้อนุมัติสำรองแทนชั่วคราวได้</p>
                    <form id="delegateForm" onsubmit="saveDelegateSettings(event)">
                        <div class="mb-3">
                            <label class="form-label fw-bold">เลือกพนักงานปฏิบัติหน้าที่แทน (Backup Approver):</label>
                            <select id="delegateEmpSelect" class="form-select" required>
                                <!-- Dynamic -->
                            </select>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold small">ตั้งแต่วันที่:</label>
                                <input type="date" id="delegateStartDate" class="form-control" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold small">ถึงวันที่:</label>
                                <input type="date" id="delegateEndDate" class="form-control" required>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between">
                            <button type="button" class="btn btn-outline-danger btn-sm" onclick="clearDelegateSettings()">ยกเลิกการมอบหมาย</button>
                            <button type="submit" class="btn btn-dark btn-sm fw-bold px-4">บันทึกการมอบหมาย</button>
                        </div>
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
            "COMP01": "1. บริษัท เทคโนโลยี นวัตกรรม จำกัด",
            "COMP02": "2. บริษัท การตลาด สร้างสรรค์ จำกัด",
            "COMP03": "3. บริษัท การเงิน มั่นคง จำกัด",
            "COMP04": "4. บริษัท ดีไซน์ สตูดิโอ จำกัด",
            "COMP05": "5. บริษัท โลจิสติกส์ ไทย จำกัด"
        };

        const defaultApprovers = {
            "APPR001": { id: "APPR001", companyId: "COMP01", name: "ดร.วิกรม นวัตกรรม", position: "HR Admin / ผู้จัดการทั่วไป", pass: "1234" },
            "APPR002": { id: "APPR002", companyId: "COMP02", name: "คุณวิภาดา การตลาด", position: "HR Admin / ผู้อำนวยการ", pass: "1234" },
            "APPR003": { id: "APPR003", companyId: "COMP03", name: "คุณสมศักดิ์ การเงิน", position: "HR Admin / CFO", pass: "1234" },
            "APPR004": { id: "APPR004", companyId: "COMP04", name: "คุณณัฐกาญจน์ ดีไซน์", position: "HR Admin / ผู้อำนวยการ", pass: "1234" },
            "APPR005": { id: "APPR005", companyId: "COMP05", name: "คุณเกรียงไกร โลจิสติกส์", position: "HR Admin / ผู้จัดการ", pass: "1234" }
        };

        const defaultEmployees = {
            "EMP001": { id: "EMP001", companyId: "COMP01", name: "นายสมชาย สายชิว", dept: "ฝ่ายพัฒนาระบบ", pass: "1234", email: "somchai@company.co.th", quotas: { "ลาพักร้อน": {total: 12, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP002": { id: "EMP002", companyId: "COMP01", name: "นายวิชัย ใจดี", dept: "ฝ่ายพัฒนาระบบ", pass: "1234", email: "wichai@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP003": { id: "EMP003", companyId: "COMP01", name: "นายอนันต์ มั่นคง", dept: "ฝ่ายทดสอบระบบ", pass: "1234", email: "anan@company.co.th", quotas: { "ลาพักร้อน": {total: 15, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 8, used: 0} } },

            "EMP004": { id: "EMP004", companyId: "COMP02", name: "นางสาวสมหญิง จริงใจ", dept: "ฝ่ายวางแผนสื่อ", pass: "1234", email: "somying@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP005": { id: "EMP005", companyId: "COMP02", name: "นางสาวนภา แจ่มใส", dept: "ฝ่ายคอนเทนต์", pass: "1234", email: "napa@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP006": { id: "EMP006", companyId: "COMP02", name: "นางสาวกานดา นวลหงส์", dept: "ฝ่ายโฆษณาออนไลน์", pass: "1234", email: "kanda@company.co.th", quotas: { "ลาพักร้อน": {total: 12, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },

            "EMP007": { id: "EMP007", companyId: "COMP03", name: "นายธีรภัทร ยอดเยี่ยม", dept: "ฝ่ายบัญชีการเงิน", pass: "1234", email: "theerapat@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP008": { id: "EMP008", companyId: "COMP03", name: "นายเมธา ปัญญาดี", dept: "ฝ่ายวิเคราะห์การลงทุน", pass: "1234", email: "metha@company.co.th", quotas: { "ลาพักร้อน": {total: 14, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP009": { id: "EMP009", companyId: "COMP03", name: "นางสาวชลธิชา สุขสันต์", dept: "ฝ่ายตรวจสอบภายใน", pass: "1234", email: "cholthicha@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },

            "EMP010": { id: "EMP010", companyId: "COMP04", name: "นายกิตติ ศิลป์งาม", dept: "ฝ่าย UI/UX Design", pass: "1234", email: "kitti@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP011": { id: "EMP011", companyId: "COMP04", name: "นางสาวปรียา สดใส", dept: "ฝ่าย Graphic Design", pass: "1234", email: "preeya@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP012": { id: "EMP012", companyId: "COMP04", name: "นายณัฐพล สร้างสรรค์", dept: "ฝ่าย 3D & Animation", pass: "1234", email: "nattapon@company.co.th", quotas: { "ลาพักร้อน": {total: 12, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },

            "EMP013": { id: "EMP013", companyId: "COMP05", name: "นางสาวศิริพร ว่องไว", dept: "ฝ่ายจัดการคลังสินค้า", pass: "1234", email: "siriporn@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP014": { id: "EMP014", companyId: "COMP05", name: "นายธนกร ส่งไว", dept: "ฝ่ายวางแผนการขนส่ง", pass: "1234", email: "thanakorn@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } },
            "EMP015": { id: "EMP015", companyId: "COMP05", name: "นายวรวุฒิ ตรงเวลา", dept: "ฝ่ายประสานงานกระจายสินค้า", pass: "1234", email: "worawut@company.co.th", quotas: { "ลาพักร้อน": {total: 10, used: 0}, "ลาป่วย": {total: 30, used: 0}, "ลากิจ": {total: 6, used: 0} } }
        };

        const thaiPublicHolidays = [
            "01-01", "02-26", "04-06", "04-13", "04-14", "04-15",
            "05-01", "05-04", "06-03", "07-28", "08-12", "10-13",
            "10-23", "12-05", "12-10", "12-31"
        ];

        let activeLeaveIdForApproval = null;
        let currentActiveFileData = null;
        let currentActiveFileName = null;
        let currentManagingCompanyId = null;

        let calendarYear = new Date().getFullYear();
        let calendarMonth = new Date().getMonth();

        function initData() {
            if (!localStorage.getItem("v15_leaveTypes")) {
                localStorage.setItem("v15_leaveTypes", JSON.stringify(defaultLeaveTypes));
                localStorage.setItem("v15_companies", JSON.stringify(defaultCompanies));
                localStorage.setItem("v15_approvers", JSON.stringify(defaultApprovers));
                localStorage.setItem("v15_employees", JSON.stringify(defaultEmployees));
                localStorage.setItem("v15_leaveRequests", JSON.stringify([]));
                localStorage.setItem("v15_delegates", JSON.stringify({}));
            }
            populateLoginDropdowns();
            checkSession();
        }

        function getLeaveTypes() { return JSON.parse(localStorage.getItem("v15_leaveTypes")); }
        function saveLeaveTypes(data) { localStorage.setItem("v15_leaveTypes", JSON.stringify(data)); }
        function getCompanies() { return JSON.parse(localStorage.getItem("v15_companies")); }
        function getApprovers() { return JSON.parse(localStorage.getItem("v15_approvers")); }
        function getEmployees() { return JSON.parse(localStorage.getItem("v15_employees")); }
        function saveEmployees(data) { localStorage.setItem("v15_employees", JSON.stringify(data)); }
        function getRequests() { return JSON.parse(localStorage.getItem("v15_leaveRequests")); }
        function saveRequests(data) { localStorage.setItem("v15_leaveRequests", JSON.stringify(data)); }
        function getSession() { return JSON.parse(localStorage.getItem("v15_session")); }
        function saveSession(session) { localStorage.setItem("v15_session", JSON.stringify(session)); }
        function getDelegates() { return JSON.parse(localStorage.getItem("v15_delegates") || "{}"); }
        function saveDelegates(data) { localStorage.setItem("v15_delegates", JSON.stringify(data)); }

        function populateLoginDropdowns() {
            const companies = getCompanies();
            const empCompSelect = document.getElementById("loginCompanySelect");
            const apprCompSelect = document.getElementById("loginApprCompanySelect");
            
            empCompSelect.innerHTML = "";
            apprCompSelect.innerHTML = "";

            for (let cId in companies) {
                empCompSelect.innerHTML += `<option value="${cId}">${companies[cId]}</option>`;
                apprCompSelect.innerHTML += `<option value="${cId}">${companies[cId]}</option>`;
            }
            onLoginCompanyChange("COMP01");
            onLoginApprCompanyChange("COMP01");
        }

        function onLoginCompanyChange(cId) {
            const employees = getEmployees();
            const userSelect = document.getElementById("loginUserSelect");
            userSelect.innerHTML = "";

            for (let eId in employees) {
                if (employees[eId].companyId === cId) {
                    userSelect.innerHTML += `<option value="${eId}">${employees[eId].name} (${employees[eId].dept})</option>`;
                }
            }
        }

        function onLoginApprCompanyChange(cId) {
            const approvers = getApprovers();
            const apprSelect = document.getElementById("loginApprUserSelect");
            apprSelect.innerHTML = "";

            for (let aId in approvers) {
                if (approvers[aId].companyId === cId) {
                    apprSelect.innerHTML += `<option value="${aId}">${approvers[aId].name} - ${approvers[aId].position}</option>`;
                }
            }

            const delegates = getDelegates();
            const delInfo = delegates[cId];
            if (delInfo && delInfo.empId) {
                const todayStr = new Date().toISOString().split('T')[0];
                if (todayStr >= delInfo.startDate && todayStr <= delInfo.endDate) {
                    apprSelect.innerHTML += `<option value="${delInfo.empId}" class="text-success fw-bold">👉 [ผู้ปฏิบัติหน้าที่แทน] ${delInfo.empName} (Delegate Active)</option>`;
                }
            }
        }

        function handleEmployeeLogin(e) {
            e.preventDefault();
            const empId = document.getElementById("loginUserSelect").value;
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
            const pass = document.getElementById("apprPassword").value;
            const approvers = getApprovers();
            const employees = getEmployees();
            const companyId = document.getElementById("loginApprCompanySelect").value;

            let isDelegateUser = false;
            const delegates = getDelegates();
            const delInfo = delegates[companyId];
            if (delInfo && delInfo.empId === apprId) {
                isDelegateUser = true;
            }

            let correctPass = "1234";
            if (!isDelegateUser && approvers[apprId]) {
                correctPass = approvers[apprId].pass || "1234";
            } else if (isDelegateUser && employees[apprId]) {
                correctPass = employees[apprId].pass || "1234";
            }

            if (pass !== correctPass) {
                alert("รหัสผ่านไม่ถูกต้อง! (รหัสผ่านเริ่มต้นคือ 1234)");
                return;
            }

            if (isDelegateUser) {
                saveSession({ role: "approver", apprId: apprId, isDelegate: true, companyId: companyId });
            } else {
                saveSession({ role: "approver", apprId: apprId, isDelegate: false });
            }

            document.getElementById("apprPassword").value = "";
            checkSession();
        }

        function handleLogout() {
            localStorage.removeItem("v15_session");
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
                    renderApproverView(session.apprId, session.isDelegate, session.companyId);
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

            document.getElementById("empInfoCompany").innerText = companies[emp.companyId];
            document.getElementById("empInfoName").innerText = emp.name;
            document.getElementById("empInfoDept").innerText = `รหัส: ${emp.id} | แผนก: ${emp.dept}`;

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

        // ==================== SMART WARNING & OVERLAP CHECK LOGIC ====================
        function checkDepartmentCapacityOverlap(empId, startDateStr, endDateStr) {
            if (!startDateStr || !endDateStr) return { isOver50: false, overlapNames: [] };

            const employees = getEmployees();
            const currentEmp = employees[empId];
            if (!currentEmp) return { isOver50: false, overlapNames: [] };

            let deptEmpIds = [];
            for (let id in employees) {
                if (employees[id].companyId === currentEmp.companyId && employees[id].dept === currentEmp.dept) {
                    deptEmpIds.push(id);
                }
            }
            const totalDeptStaff = deptEmpIds.length;
            if (totalDeptStaff <= 1) return { isOver50: false, overlapNames: [] };

            const requests = getRequests();
            let startReq = new Date(startDateStr);
            let endReq = new Date(endDateStr);

            let overlappingStaffSet = new Set();

            requests.forEach(req => {
                if (req.companyId === currentEmp.companyId && req.empId !== empId && (req.status === "Approved" || req.status === "Pending")) {
                    let reqEmp = employees[req.empId];
                    if (reqEmp && reqEmp.dept === currentEmp.dept) {
                        let rStart = new Date(req.startDate);
                        let rEnd = new Date(req.endDate);
                        if (startReq <= rEnd && endReq >= rStart) {
                            overlappingStaffSet.add(req.empId);
                        }
                    }
                }
            });

            let countOverlapping = overlappingStaffSet.size;
            let totalOnLeave = countOverlapping + 1;
            let ratio = totalOnLeave / totalDeptStaff;

            let overlapNamesArr = [];
            overlappingStaffSet.forEach(id => {
                if (employees[id]) overlapNamesArr.push(employees[id].name);
            });

            return {
                isOver50: ratio > 0.5,
                ratioPercent: Math.round(ratio * 100),
                overlapNames: overlapNamesArr,
                totalOnLeave: totalOnLeave,
                totalDeptStaff: totalDeptStaff
            };
        }

        function calculateDays() {
            const session = getSession();
            const isHalf = document.getElementById("modeHalf").checked;
            const startVal = document.getElementById("startDate").value;
            const endVal = document.getElementById("endDate").value;
            const textElem = document.getElementById("calculatedDaysText");
            const warningBox = document.getElementById("liveOverlapWarning");
            const warningText = document.getElementById("overlapWarningText");

            let days = 0;
            if (isHalf) {
                if (startVal) {
                    textElem.innerText = `0.5 วัน (ลาครึ่งวัน)`;
                    textElem.className = "fw-bold fs-4 text-primary";
                    days = 0.5;
                } else {
                    textElem.innerText = "0 วัน";
                    textElem.className = "fw-bold fs-4 text-primary";
                    days = 0;
                }
            } else {
                if (startVal && endVal) {
                    let start = new Date(startVal);
                    let end = new Date(endVal);

                    if (end >= start) {
                        let validDaysCount = 0;
                        let curDate = new Date(start);

                        while (curDate <= end) {
                            const dayOfWeek = curDate.getDay();
                            const monthDay = String(curDate.getMonth() + 1).padStart(2, '0') + '-' + String(curDate.getDate()).padStart(2, '0');
                            const isSunday = (dayOfWeek === 0);
                            const isHoliday = thaiPublicHolidays.includes(monthDay);

                            if (!isSunday && !isHoliday) {
                                validDaysCount++;
                            }
                            curDate.setDate(curDate.getDate() + 1);
                        }

                        textElem.innerText = `${validDaysCount} วัน`;
                        textElem.className = "fw-bold fs-4 text-primary";
                        days = validDaysCount;
                    } else {
                        textElem.innerText = "วันที่สิ้นสุดต้องไม่น้อยกว่าวันที่เริ่มต้น!";
                        textElem.className = "fw-bold fs-6 text-danger";
                        days = 0;
                    }
                } else {
                    textElem.innerText = "0 วัน";
                    textElem.className = "fw-bold fs-4 text-primary";
                    days = 0;
                }
            }

            if (session && session.empId && startVal) {
                let checkEnd = isHalf ? startVal : (endVal || startVal);
                const capacityCheck = checkDepartmentCapacityOverlap(session.empId, startVal, checkEnd);
                if (capacityCheck.isOver50) {
                    warningText.innerHTML = `มีพนักงานในแผนกเดียวกันลาในช่วงเวลานี้ถึง <strong>${capacityCheck.totalOnLeave} จาก ${capacityCheck.totalDeptStaff} คน (${capacityCheck.ratioPercent}%)</strong> ได้แก่: [${capacityCheck.overlapNames.join(', ')}] ซึ่งเกิน 50% อาจส่งผลกระทบต่อการปฏิบัติงาน`;
                    warningBox.classList.remove("d-none");
                } else {
                    warningBox.classList.add("d-none");
                }
            } else {
                warningBox.classList.add("d-none");
            }

            return days;
        }

        function renderApproverView(apprId, isDelegate = false, delegateCompanyId = null) {
            const approvers = getApprovers();
            const employees = getEmployees();
            const companies = getCompanies();

            let apprName = "";
            let apprPos = "";
            let companyId = "";

            if (isDelegate) {
                const empObj = employees[apprId];
                apprName = empObj ? empObj.name : "ผู้ปฏิบัติหน้าที่แทน";
                apprPos = "ผู้อนุมัติสำรอง (Delegate Approver)";
                companyId = delegateCompanyId;
            } else {
                const apprObj = approvers[apprId] || { name: "HR Admin", position: "ผู้จัดการ", companyId: "COMP01" };
                apprName = apprObj.name;
                apprPos = apprObj.position;
                companyId = apprObj.companyId;
            }

            currentManagingCompanyId = companyId;

            document.getElementById("navUserName").innerText = apprName;
            document.getElementById("navUserRole").innerText = `${apprPos} | ${companies[companyId] || ''}`;
            document.getElementById("approverCompanyText").innerText = companies[companyId] || 'บริษัท';

            const delegates = getDelegates();
            const delInfo = delegates[companyId];
            const banner = document.getElementById("delegateAlertBanner");
            if (delInfo && delInfo.empId) {
                banner.classList.remove("d-none");
                document.getElementById("delegateActiveName").innerText = delInfo.empName;
                document.getElementById("delegateStartText").innerText = delInfo.startDate;
                document.getElementById("delegateEndText").innerText = delInfo.endDate;
            } else {
                banner.classList.add("d-none");
            }

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

            const requests = getRequests().filter(r => r.companyId === currentManagingCompanyId && r.status === "Approved");

            let leaveDaysMap = {};
            requests.forEach(req => {
                let cur = new Date(req.startDate);
                let end = new Date(req.endDate);
                while (cur <= end) {
                    const y = cur.getFullYear();
                    const m = String(cur.getMonth() + 1).padStart(2, '0');
                    const d = String(cur.getDate()).padStart(2, '0');
                    const dateStr = `${y}-${m}-${d}`;

                    if (!leaveDaysMap[dateStr]) leaveDaysMap[dateStr] = [];
                    leaveDaysMap[dateStr].push({ name: req.empName, type: req.type, isHalf: req.isHalf, halfSession: req.halfSession });

                    cur.setDate(cur.getDate() + 1);
                }
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
                            leaveDaysMap[fullDateStr].forEach(leave => {
                                let badgeBg = "bg-primary text-white";
                                if (leave.type === "ลาป่วย") badgeBg = "bg-success text-white";
                                else if (leave.type === "ลากิจ") badgeBg = "bg-warning text-dark";

                                let subText = "";
                                if (leave.isHalf) {
                                    subText = leave.halfSession === "morning" ? " (ครึ่งเช้า)" : " (ครึ่งบ่าย)";
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
                tbody.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-3">ไม่พบข้อมูลพนักงานในบริษัทนี้</td></tr>`;
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
                                <button class="btn btn-sm btn-outline-dark py-0" onclick="openChangePasswordModal('${emp.id}')"><i class="bi bi-key me-1"></i> เปลี่ยนรหัสผ่าน</button>
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
            renderApproverView(getSession().apprId, getSession().isDelegate, getSession().companyId);
        }

        function openDelegateModal() {
            const employees = getEmployees();
            const select = document.getElementById("delegateEmpSelect");
            select.innerHTML = "";

            for (let eId in employees) {
                if (employees[eId].companyId === currentManagingCompanyId) {
                    select.innerHTML += `<option value="${eId}">${employees[eId].name} (${employees[eId].dept})</option>`;
                }
            }

            const delegates = getDelegates();
            const curDel = delegates[currentManagingCompanyId];
            if (curDel) {
                select.value = curDel.empId;
                document.getElementById("delegateStartDate").value = curDel.startDate || "";
                document.getElementById("delegateEndDate").value = curDel.endDate || "";
            } else {
                document.getElementById("delegateStartDate").value = "";
                document.getElementById("delegateEndDate").value = "";
            }

            const modal = new bootstrap.Modal(document.getElementById('delegateModal'));
            modal.show();
        }

        function saveDelegateSettings(e) {
            e.preventDefault();
            const empId = document.getElementById("delegateEmpSelect").value;
            const startDate = document.getElementById("delegateStartDate").value;
            const endDate = document.getElementById("delegateEndDate").value;
            const employees = getEmployees();
            const emp = employees[empId];

            if (!emp) return;

            let delegates = getDelegates();
            delegates[currentManagingCompanyId] = {
                empId: empId,
                empName: emp.name,
                startDate: startDate,
                endDate: endDate
            };
            saveDelegates(delegates);

            bootstrap.Modal.getInstance(document.getElementById('delegateModal')).hide();
            alert(`ตั้งค่าผู้อนุมัติสำรองเป็น "${emp.name}" เรียบร้อยแล้ว`);
            populateLoginDropdowns();
            renderApproverView(getSession().apprId, getSession().isDelegate, getSession().companyId);
        }

        function clearDelegateSettings() {
            if (!confirm("คุณต้องการยกเลิกการมอบหมายผู้อนุมัติสำรองใช่หรือไม่?")) return;

            let delegates = getDelegates();
            delete delegates[currentManagingCompanyId];
            saveDelegates(delegates);

            bootstrap.Modal.getInstance(document.getElementById('delegateModal')).hide();
            alert("ยกเลิกการมอบหมายเรียบร้อยแล้ว");
            populateLoginDropdowns();
            renderApproverView(getSession().apprId, getSession().isDelegate, getSession().companyId);
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
                renderApproverView(getSession().apprId, getSession().isDelegate, getSession().companyId);
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
            renderApproverView(getSession().apprId, getSession().isDelegate, getSession().companyId);
        }

        function toggleReasonField() {
            const leaveType = document.getElementById("leaveType").value;
            const leaveReason = document.getElementById("leaveReason");
            leaveReason.placeholder = `ระบุรายละเอียด/เหตุผลสำหรับการขอ "${leaveType || 'ลางาน'}"...`;
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
                alert("จำนวนวันลาจริงเป็น 0 วัน กรุณาตรวจสอบช่วงวันที่เลือกอีกครั้ง");
                return;
            }

            const leaveType = document.getElementById("leaveType").value;
            const leaveReason = document.getElementById("leaveReason").value;
            const startDate = document.getElementById("startDate").value;
            const endDate = isHalf ? startDate : document.getElementById("endDate").value;
            const fileInput = document.getElementById("leaveFile");

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

            const capCheck = checkDepartmentCapacityOverlap(currentEmp.id, startDate, endDate);
            let isHighOverlap = capCheck.isOver50;

            const saveAndFinish = (fileDataUrl, fileName) => {
                const newRequest = {
                    id: "LV-" + Date.now().toString().slice(-5),
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
                    fileName: fileName,
                    fileData: fileDataUrl,
                    createdAt: new Date().toLocaleDateString("th-TH"),
                    status: "Pending",
                    approvedBy: "-",
                    rejectionReason: "",
                    hasCapacityWarning: isHighOverlap
                };

                const requests = getRequests();
                requests.unshift(newRequest);
                saveRequests(requests);

                document.getElementById("leaveForm").reset();
                document.getElementById("modeFull").checked = true;
                onDurationModeChange();
                document.getElementById("calculatedDaysText").innerText = "0 วัน";
                document.getElementById("liveOverlapWarning").classList.add("d-none");
                
                let alertMsg = "🔔 ส่งคำขอลางานสำเร็จ! ระบบได้ส่ง Notification แจ้งเตือนไปยังผู้อนุมัติเรียบร้อยแล้ว";
                if (isHighOverlap) {
                    alertMsg = "⚠️ ส่งคำขอลางานสำเร็จ (ระบบบันทึกคำเตือน: มีพนักงานในแผนกเดียวกันลาในช่วงเวลานี้เกิน 50%)";
                }
                alert(alertMsg);
                renderEmployeeView(session.empId);
            };

            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                const reader = new FileReader();
                reader.onload = function(evt) {
                    saveAndFinish(evt.target.result, file.name);
                };
                reader.readAsDataURL(file);
            } else {
                saveAndFinish(null, "ไม่มีไฟล์แนบ");
            }
        }

        function handleCancelRequest(requestId) {
            if (!confirm("คุณต้องการยกเลิกคำขอลางานนี้ใช่หรือไม่?")) return;

            let requests = getRequests();
            const reqIndex = requests.findIndex(r => r.id === requestId);

            if (reqIndex !== -1) {
                if (requests[reqIndex].status !== "Pending") {
                    alert("ไม่สามารถยกเลิกคำขอนี้ได้ เนื่องจากไม่อยู่ในสถานะรออนุมัติ");
                    return;
                }

                requests[reqIndex].status = "Cancelled";
                requests[reqIndex].approvedBy = "ยกเลิกโดยพนักงานเอง";
                saveRequests(requests);

                alert("ยกเลิกคำขอลางานเรียบร้อยแล้ว");
                renderEmployeeView(getSession().empId);
            }
        }

        function renderEmployeeHistory(empId) {
            const requests = getRequests().filter(r => r.empId === empId);
            const tbody = document.getElementById("employeeHistoryTable");
            tbody.innerHTML = "";

            if (requests.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-4">ไม่พบบันทึกการลางาน</td></tr>`;
                return;
            }

            requests.forEach(req => {
                let badgeClass = "bg-warning text-dark";
                let statusTh = "รออนุมัติ";
                if (req.status === "Approved") { badgeClass = "bg-success"; statusTh = "อนุมัติแล้ว"; }
                else if (req.status === "Rejected") { badgeClass = "bg-danger"; statusTh = "ไม่อนุมัติ"; }
                else if (req.status === "Cancelled") { badgeClass = "bg-secondary"; statusTh = "ยกเลิกแล้ว"; }

                let actionBtn = req.status === "Pending" ? 
                    `<button class="btn btn-outline-danger btn-sm px-2 py-1" onclick="handleCancelRequest('${req.id}')"><i class="bi bi-x-circle me-1"></i> ยกเลิก</button>` : 
                    `<span class="text-muted small">${statusTh}</span>`;

                let rejectionInfo = "";
                if (req.status === "Rejected" && req.rejectionReason) {
                    rejectionInfo = `<div class="text-danger small mt-1"><i class="bi bi-info-circle-fill me-1"></i><strong>เหตุผลที่ไม่อนุมัติ:</strong> ${req.rejectionReason}</div>`;
                }

                let typeDisplay = req.type;
                if (req.isHalf) {
                    let sText = req.halfSession === 'morning' ? 'ครึ่งวันเช้า' : 'ครึ่งวันบ่าย';
                    typeDisplay += ` <br><span class="badge bg-light text-primary border">${sText}</span>`;
                }

                tbody.innerHTML += `
                    <tr>
                        <td><small class="text-muted">${req.createdAt}</small></td>
                        <td><span class="fw-bold">${typeDisplay}</span></td>
                        <td><small>${req.startDate}${req.startDate !== req.endDate ? '<br>ถึง ' + req.endDate : ''}</small></td>
                        <td><span class="badge bg-info text-dark fw-bold">${req.totalDays} วัน</span></td>
                        <td>
                            <span class="badge ${badgeClass} status-badge">${statusTh}</span>
                            ${rejectionInfo}
                        </td>
                        <td><small class="fw-bold text-secondary">${req.approvedBy || '-'}</small></td>
                        <td class="text-center">${actionBtn}</td>
                    </tr>
                `;
            });
        }

        function renderApproverTable(approverCompanyId) {
            let requests = getRequests().filter(r => r.companyId === approverCompanyId);
            
            let pendingRequests = requests.filter(r => r.status === "Pending");
            let pendingCount = pendingRequests.length;

            const banner = document.getElementById("approverNotificationBanner");
            const countBadgeTop = document.getElementById("pendingNotificationCount");
            const countBadgeTable = document.getElementById("pendingBadgeCount");

            if (pendingCount > 0) {
                banner.classList.remove("d-none");
                banner.classList.add("d-flex");
                countBadgeTop.innerText = pendingCount;
                countBadgeTable.innerText = `${pendingCount} รายการรออนุมัติ`;
                countBadgeTable.className = "badge bg-danger rounded-pill px-2 py-1 me-2 shadow-sm animate-pulse";
            } else {
                banner.classList.remove("d-flex");
                banner.classList.add("d-none");
                countBadgeTable.innerText = "ไม่มีรายการรออนุมัติ";
                countBadgeTable.className = "badge bg-secondary rounded-pill px-2 py-1 me-2";
            }

            const tbody = document.getElementById("approverTable");
            tbody.innerHTML = "";

            if (requests.length === 0) {
                tbody.innerHTML = `<tr><td colspan="9" class="text-center text-muted py-4">ยังไม่มีคำขอลางานในบริษัทนี้</td></tr>`;
                return;
            }

            requests.forEach(req => {
                let badgeClass = "bg-warning text-dark";
                let statusTh = "รออนุมัติ";
                if (req.status === "Approved") { badgeClass = "bg-success"; statusTh = "อนุมัติแล้ว"; }
                else if (req.status === "Rejected") { badgeClass = "bg-danger"; statusTh = "ไม่อนุมัติ"; }
                else if (req.status === "Cancelled") { badgeClass = "bg-secondary"; statusTh = "ยกเลิกแล้ว"; }

                let rejectReasonDisplay = (req.status === "Rejected" && req.rejectionReason) ? `<br><small class="text-danger">เหตุผล: ${req.rejectionReason}</small>` : "";

                let capacityWarningBadge = "";
                if (req.hasCapacityWarning) {
                    capacityWarningBadge = `<br><span class="badge bg-warning text-dark mt-1" title="มีคนลาในแผนกเดียวกันเกิน 50%"><i class="bi bi-exclamation-triangle-fill"></i> แผนกคนลาเกิน 50%</span>`;
                }

                let typeDisplay = req.type;
                if (req.isHalf) {
                    let sText = req.halfSession === 'morning' ? 'ครึ่งวันเช้า' : 'ครึ่งวันบ่าย';
                    typeDisplay += ` <br><span class="badge bg-light text-primary border">${sText}</span>`;
                }

                let rowHighlight = req.status === 'Pending' ? 'table-warning' : '';

                tbody.innerHTML += `
                    <tr class="${rowHighlight}">
                        <td><strong>${req.id}</strong></td>
                        <td><small class="badge bg-secondary">${req.companyName || 'N/A'}</small></td>
                        <td>${req.empName} <br><small class="text-muted">${req.empDept}</small></td>
                        <td>${typeDisplay}</td>
                        <td><small>${req.startDate}${req.startDate !== req.endDate ? ' ถึง <br>' + req.endDate : ''}</small></td>
                        <td><span class="badge bg-primary">${req.totalDays} วัน</span></td>
                        <td><span class="badge ${badgeClass} status-badge">${statusTh}</span>${rejectReasonDisplay}${capacityWarningBadge}</td>
                        <td><small class="fw-bold text-secondary">${req.approvedBy || '-'}</small></td>
                        <td class="text-center">
                            ${req.status === 'Pending' ? `<button class="btn btn-sm btn-primary fw-bold px-3 py-1 shadow-sm" onclick="openDetailModal('${req.id}')"><i class="bi bi-eye-fill me-1"></i> ตรวจสอบ</button>` : `<span class="text-muted small">${statusTh}</span>`}
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
            renderApproverView(getSession().apprId, getSession().isDelegate, getSession().companyId);
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
            renderApproverView(getSession().apprId, getSession().isDelegate, getSession().companyId);
        }

        function deleteLeaveType(lKey) {
            if (!confirm(`คุณต้องการลบประเภทการลา "${lKey}" ใช่หรือไม่?`)) return;

            let leaveTypes = getLeaveTypes();
            delete leaveTypes[lKey];
            saveLeaveTypes(leaveTypes);

            renderLeaveTypesConfigTable();
            alert("ลบประเภทการลาเรียบร้อยแล้ว");
            renderApproverView(getSession().apprId, getSession().isDelegate, getSession().companyId);
        }

        function openDetailModal(requestId) {
            activeLeaveIdForApproval = requestId;
            const req = getRequests().find(r => r.id === requestId);
            if (!req) return;

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

            const modalOverlapBox = document.getElementById("modalOverlapWarningBox");
            if (req.hasCapacityWarning) {
                modalOverlapBox.classList.remove("d-none");
            } else {
                modalOverlapBox.classList.add("d-none");
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
                const employees = getEmployees();
                
                let approverTitle = "HR Admin";
                if (session.isDelegate) {
                    const empObj = employees[session.apprId];
                    approverTitle = empObj ? `${empObj.name} (ผู้อนุมัติสำรอง)` : "ผู้อนุมัติสำรอง";
                } else {
                    const curAppr = approvers[session.apprId];
                    approverTitle = curAppr ? `${curAppr.name} (${curAppr.position})` : "HR Admin";
                }

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

                let approverTitle = "HR Admin";
                if (session.isDelegate) {
                    const empObj = employees[session.apprId];
                    approverTitle = empObj ? `${empObj.name} (ผู้อนุมัติสำรอง)` : "ผู้อนุมัติสำรอง";
                } else {
                    const curAppr = approvers[session.apprId];
                    approverTitle = curAppr ? `${curAppr.name} (${curAppr.position})` : "HR Admin";
                }

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

        function showEmailSimulation(req, status, approverName) {
            const isApproved = (status === "Approved");
            const emailTo = req.empEmail || (req.empId.toLowerCase() + "@company.co.th");
            
            document.getElementById("simEmailTo").innerText = emailTo;
            document.getElementById("simEmailSubject").innerText = isApproved ? 
                `[แจ้งผลการพิจารณา] คำขอลา "${req.type}" ของคุณได้รับการอนุมัติแล้ว` : 
                `[แจ้งผลการพิจารณา] คำขอลา "${req.type}" ของคุณไม่ได้รับการอนุมัติ`;
            
            document.getElementById("simEmpName").innerText = req.empName;
            
            let messageText = "";
            if (isApproved) {
                messageText = `ขอแจ้งให้ทราบว่า คำขอลางานประเภท "${req.type}" ของท่าน (ช่วงวันที่ ${req.startDate} ถึง ${req.endDate}, จำนวน ${req.totalDays} วัน) ได้รับการอนุมัติเรียบร้อยแล้ว`;
            } else {
                messageText = `ขอแจ้งให้ทราบว่า คำขอลางานประเภท "${req.type}" ของท่าน ไม่ได้รับการอนุมัติ เนื่องจาก: "${req.rejectionReason || 'ติดภาระกิจงานด่วน'}"`;
            }
            document.getElementById("simEmailMessage").innerText = messageText;
            document.getElementById("simLeaveDetails").innerText = `${req.type} (${req.totalDays} วัน | ${req.startDate} ถึง ${req.endDate})`;
            document.getElementById("simApproverName").innerText = approverName;

            const emailModal = new bootstrap.Modal(document.getElementById('emailSimulationModal'));
            emailModal.show();

            const emailModalEl = document.getElementById('emailSimulationModal');
            emailModalEl.addEventListener('hidden.bs.modal', function () {
                const session = getSession();
                if (session && session.role === "approver") {
                    renderApproverView(session.apprId, session.isDelegate, session.companyId);
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