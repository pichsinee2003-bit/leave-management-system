# utils.py - จัดการข้อมูลและตรรกะธุรกิจทั้งหมดด้วยภาษา Python

import datetime

# ข้อมูลจำลองตั้งต้น (Mock Database ในฝั่ง Python)
DB_LEAVE_TYPES = {
    "ลาพักร้อน": {"name": "ลาพักร้อน", "defaultQuota": 10, "color": "text-primary"},
    "ลาป่วย": {"name": "ลาป่วย", "defaultQuota": 30, "color": "text-success"},
    "ลากิจ": {"name": "ลากิจ", "defaultQuota": 6, "color": "text-warning"}
}

DB_COMPANIES = {
    "COMP01": "1. บริษัท เทคโนโลยี นวัตกรรม จำกัด",
    "COMP02": "2. บริษัท การตลาด สร้างสรรค์ จำกัด",
    "COMP03": "3. บริษัท การเงิน มั่นคง จำกัด",
    "COMP04": "4. บริษัท ดีไซน์ สตูดิโอ จำกัด",
    "COMP05": "5. บริษัท โลจิสติกส์ ไทย จำกัด"
}

DB_APPROVERS = {
    "APPR001": {"id": "APPR001", "companyId": "COMP01", "name": "ดร.วิกรม นวัตกรรม", "position": "HR Admin / ผู้จัดการทั่วไป", "pass": "1234"},
    "APPR002": {"id": "APPR002", "companyId": "COMP02", "name": "คุณวิภาดา การตลาด", "position": "HR Admin / ผู้อำนวยการ", "pass": "1234"},
    "APPR003": {"id": "APPR003", "companyId": "COMP03", "name": "คุณสมศักดิ์ การเงิน", "position": "HR Admin / CFO", "pass": "1234"},
    "APPR004": {"id": "APPR004", "companyId": "COMP04", "name": "คุณณัฐกาญจน์ ดีไซน์", "position": "HR Admin / ผู้อำนวยการ", "pass": "1234"},
    "APPR005": {"id": "APPR005", "companyId": "COMP05", "name": "คุณเกรียงไกร โลจิสติกส์", "position": "HR Admin / ผู้จัดการ", "pass": "1234"}
}

DB_EMPLOYEES = {
    "EMP001": {"id": "EMP001", "companyId": "COMP01", "name": "นายสมชาย สายชิว", "dept": "ฝ่ายพัฒนาระบบ", "pass": "1234", "email": "somchai@company.co.th", "quotas": {"ลาพักร้อน": {"total": 12, "used": 0}, "ลาป่วย": {"total": 30, "used": 0}, "ลากิจ": {"total": 6, "used": 0}}},
    "EMP002": {"id": "EMP002", "companyId": "COMP01", "name": "นายวิชัย ใจดี", "dept": "ฝ่ายพัฒนาระบบ", "pass": "1234", "email": "wichai@company.co.th", "quotas": {"ลาพักร้อน": {"total": 10, "used": 0}, "ลาป่วย": {"total": 30, "used": 0}, "ลากิจ": {"total": 6, "used": 0}}},
    "EMP003": {"id": "EMP003", "companyId": "COMP01", "name": "นายอนันต์ มั่นคง", "dept": "ฝ่ายทดสอบระบบ", "pass": "1234", "email": "anan@company.co.th", "quotas": {"ลาพักร้อน": {"total": 15, "used": 0}, "ลาป่วย": {"total": 30, "used": 0}, "ลากิจ": {"total": 8, "used": 0}}},
    "EMP004": {"id": "EMP004", "companyId": "COMP02", "name": "นางสาวสมหญิง จริงใจ", "dept": "ฝ่ายวางแผนสื่อ", "pass": "1234", "email": "somying@company.co.th", "quotas": {"ลาพักร้อน": {"total": 10, "used": 0}, "ลาป่วย": {"total": 30, "used": 0}, "ลากิจ": {"total": 6, "used": 0}}},
    "EMP005": {"id": "EMP005", "companyId": "COMP02", "name": "นางสาวนภา แจ่มใส", "dept": "ฝ่ายคอนเทนต์", "pass": "1234", "email": "napa@company.co.th", "quotas": {"ลาพักร้อน": {"total": 10, "used": 0}, "ลาป่วย": {"total": 30, "used": 0}, "ลากิจ": {"total": 6, "used": 0}}}
}

DB_REQUESTS = []
THAI_HOLIDAYS = ["01-01", "02-26", "04-06", "04-13", "04-14", "04-15", "05-01", "05-04", "06-03", "07-28", "08-12", "10-13", "10-23", "12-05", "12-10", "12-31"]

def calculate_working_days(start_date_str, end_date_str, is_half=False):
    """ฟังก์ชันคำนวณวันลาด้วย Python (ตัดวันอาทิตย์และวันหยุดนักขัตฤกษ์ออก)"""
    if is_half:
        return 0.5
    try:
        start = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if end < start:
            return 0
        
        valid_days = 0
        cur = start
        while cur <= end:
            is_sunday = (cur.weekday() == 6) # 6 คือวันอาทิตย์
            m_d = cur.strftime("%m-%d")
            is_holiday = m_d in THAI_HOLIDAYS
            
            if not is_sunday and not is_holiday:
                valid_days += 1
            cur += datetime.timedelta(days=1)
        return float(valid_days)
    except Exception:
        return 0.0

def check_overlap_logic(emp_id, start_date, end_date):
    """ตรรกะตรวจสอบการลาทับซ้อนในแผนกเกิน 50% ประมวลผลด้วย Python"""
    emp = DB_EMPLOYEES.get(emp_id)
    if not emp:
        return {"isOver50": False}
    
    company_id = emp["companyId"]
    dept = emp["dept"]
    
    dept_staff = [e_id for e_id, e_data in DB_EMPLOYEES.items() if e_data["companyId"] == company_id and e_data["dept"] == dept]
    total_staff = len(dept_staff)
    if total_staff <= 1:
        return {"isOver50": False}
    
    try:
        s_req = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        e_req = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        
        overlapping_set = set()
        for req in DB_REQUESTS:
            if req["companyId"] == company_id and req["empId"] != emp_id and req["status"] in ["Approved", "Pending"]:
                req_emp = DB_EMPLOYEES.get(req["empId"])
                if req_emp and req_emp["dept"] == dept:
                    r_start = datetime.datetime.strptime(req["startDate"], "%Y-%m-%d").date()
                    r_end = datetime.datetime.strptime(req["endDate"], "%Y-%m-%d").date()
                    if s_req <= r_end and e_req >= r_start:
                        overlapping_set.add(req["empId"])
                        
        total_on_leave = len(overlapping_set) + 1
        ratio = total_on_leave / total_staff
        
        names = [DB_EMPLOYEES[i]["name"] for i in overlapping_set if i in DB_EMPLOYEES]
        return {
            "isOver50": ratio > 0.5,
            "ratioPercent": round(ratio * 100),
            "totalOnLeave": total_on_leave,
            "totalDeptStaff": total_staff,
            "overlapNames": names
        }
    except Exception:
        return {"isOver50": False}

def get_system_metadata():
    return {
        "system_name": "Enterprise Leave Management System (Python Backend Driven)",
        "version": "2.0.0",
        "framework": "Flask + Python Core Logic",
        "supported_companies": len(DB_COMPANIES),
        "total_employees": len(DB_EMPLOYEES)
    }