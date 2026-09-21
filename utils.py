# utils.py - ไฟล์จัดการตรรกะและฟังก์ชันเสริมด้วยภาษา Python

def get_system_metadata():
    """คืนค่าข้อมูลรายละเอียดระบบและสถานะการทำงาน"""
    return {
        "system_name": "Enterprise Leave Management System",
        "version": "1.5.0",
        "framework": "Flask Backend",
        "supported_companies": 5,
        "features": [
            "Smart Warning (>50% department overlap detection)",
            "Team Leave Calendar View",
            "Delegate Approver System",
            "Email Notification Simulation"
        ]
    }

def calculate_working_days_logic(start_date, end_date):
    """ฟังก์ชันตัวอย่างสำหรับคำนวณวันทำงาน (จำลองการประมวลผลฝั่ง Python)"""
    if not start_date or not end_date:
        return 0
    return "Processed via Python Backend Logic"
    