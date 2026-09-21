# utils.py - จัดการข้อมูลและตรรกะธุรกิจด้วย Python

import datetime

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

def get_system_metadata():
    return {
        "system_name": "Enterprise Leave Management System (100% Python Backend)",
        "version": "2.1.0",
        "framework": "Flask + Python Modules",
        "supported_companies": len(DB_COMPANIES)
    }