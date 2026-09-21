# utils.py - ไฟล์จัดการตรรกะและฟังก์ชันเสริมด้วยภาษา Python

def get_system_metadata():
    """คืนค่าข้อมูลรายละเอียดระบบและสถานะการทำงาน"""
    return {
        "system_name": "Enterprise Leave Management System",
        "version": "1.6.0",
        "framework": "Flask Backend",
        "supported_companies": 5,
        "features": [
            "Smart Warning (>50% department overlap detection)",
            "Team Leave Calendar View",
            "Delegate Approver System",
            "Email Notification Simulation"
        ]
    }