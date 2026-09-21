# template_code.py - เก็บหน้าตาเว็บแอปพลิเคชันในรูปแบบตัวแปร Python String

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ระบบบริหารจัดการการลางาน (Python Powered)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Sarabun', sans-serif; background-color: #f4f6f9; color: #333; min-height: 100vh; }
        .login-container { max-width: 450px; width: 100%; }
        .card { border: none; border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08); }
        .card-header { background-color: #1e293b; color: #ffffff; border-top-left-radius: 12px !important; border-top-right-radius: 12px !important; font-weight: 600; }
        .nav-pills .nav-link.active { background-color: #2563eb; }
        .status-badge { font-size: 0.85rem; padding: 6px 12px; border-radius: 20px; }
        .calendar-table th { text-align: center; background-color: #f8fafc; width: 14.28%; }
        .calendar-cell { height: 115px; vertical-align: top; background-color: #ffffff; font-size: 0.82rem; }
        .calendar-cell.other-month { background-color: #f9fafb; color: #9ca3af; }
        .calendar-cell.today { background-color: #eff6ff; border: 2px solid #2563eb !important; }
        .leave-event-badge { font-size: 0.68rem; padding: 2px 4px; border-radius: 4px; margin-bottom: 2px; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: left; }
    </style>
</head>
<body>
    <div id="loginView" class="d-flex align-items-center justify-content-center min-vh-100 py-4">
        <div class="login-container px-3">
            <div class="text-center mb-4">
                <i class="bi bi-building-gear text-primary display-3"></i>
                <h3 class="fw-bold mt-2">ระบบบริหารจัดการการลางาน</h3>
                <p class="text-muted small">Python Backend Powered System</p>
            </div>
            <div class="card p-3 text-center">
                <h5 class="fw-bold text-success mb-3">🚀 ระบบพร้อมใช้งานผ่าน Python แล้ว!</h5>
                <p class="text-muted small">โปรเจกต์นี้ถูกแปลงโครงสร้างเป็นไฟล์ Python ทั้งหมดเรียบร้อย</p>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""