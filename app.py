# app.py - ควบคุมเส้นทาง API และประมวลผลหลักด้วย Python Flask

from flask import Flask, render_template, jsonify, request
from utils import (
    get_system_metadata, calculate_working_days, check_overlap_logic,
    DB_LEAVE_TYPES, DB_COMPANIES, DB_APPROVERS, DB_EMPLOYEES, DB_REQUESTS
)

app = Flask(__name__)

@app.route("/")
def index():
    meta = get_system_metadata()
    print(f"กำลังให้บริการ: {meta['system_name']} (Python Powered)")
    return render_template("index.html")

@app.route("/api/system-init", methods=["GET"])
def api_system_init():
    """API ส่งข้อมูลตั้งต้นทั้งหมดให้กับหน้าเว็บผ่าน JSON (ประมวลผลผ่าน Python)"""
    return jsonify({
        "leaveTypes": DB_LEAVE_TYPES,
        "companies": DB_COMPANIES,
        "approvers": DB_APPROVERS,
        "employees": DB_EMPLOYEES,
        "requests": DB_REQUESTS,
        "metadata": get_system_metadata()
    })

@app.route("/api/calculate-leave", methods=["POST"])
def api_calculate_leave():
    """API คำนวณวันลาและตรวจจับ Smart Warning 50% ด้วย Python"""
    data = request.json
    emp_id = data.get("empId")
    start_date = data.get("startDate")
    end_date = data.get("endDate")
    is_half = data.get("isHalf", False)
    
    total_days = calculate_working_days(start_date, end_date, is_half)
    overlap_info = check_overlap_logic(emp_id, start_date, end_date if not is_half else start_date)
    
    return jsonify({
        "totalDays": total_days,
        "overlapInfo": overlap_info
    })

@app.route("/api/submit-leave", methods=["POST"])
def api_submit_leave():
    """API บันทึกคำขอลางานผ่านระบบ Python Backend"""
    data = request.json
    emp_id = data.get("empId")
    emp = DB_EMPLOYEES.get(emp_id)
    if not emp:
        return jsonify({"success": False, "message": "ไม่พบข้อมูลพนักงาน"}), 400
        
    start_date = data.get("startDate")
    end_date = data.get("endDate")
    is_half = data.get("isHalf", False)
    total_days = calculate_working_days(start_date, end_date, is_half)
    overlap_info = check_overlap_logic(emp_id, start_date, end_date if not is_half else start_date)
    
    new_req = {
        "id": f"LV-{len(DB_REQUESTS) + 1001}",
        "companyId": emp["companyId"],
        "companyName": DB_COMPANIES.get(emp["companyId"]),
        "empId": emp["id"],
        "empName": emp["name"],
        "empDept": emp["dept"],
        "empEmail": emp["email"],
        "type": data.get("type"),
        "isHalf": is_half,
        "halfSession": data.get("halfSession"),
        "reason": data.get("reason", "ไม่ได้ระบุ"),
        "startDate": start_date,
        "endDate": end_date if not is_half else start_date,
        "totalDays": total_days,
        "fileName": data.get("fileName", "ไม่มีไฟล์แนบ"),
        "fileData": data.get("fileData"),
        "createdAt": "วันนี้",
        "status": "Pending",
        "approvedBy": "-",
        "rejectionReason": "",
        "hasCapacityWarning": overlap_info.get("isOver50", False)
    }
    
    DB_REQUESTS.insert(0, new_req)
    return jsonify({"success": True, "request": new_req})

if __name__ == "__main__":
    print("==================================================")
    print("  Leave Management System (Python Core Backend)   ")
    print("  เปิดเบราว์เซอร์ไปที่: http://127.0.0.1:5000       ")
    print("==================================================")
    app.run(debug=True, port=5000)