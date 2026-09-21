from flask import Flask, render_template, jsonify
from utils import get_system_metadata

app = Flask(__name__)

@app.route("/")
def index():
    meta = get_system_metadata()
    print(f"กำลังให้บริการระบบ: {meta['system_name']} (Version: {meta['version']})")
    return render_template("index.html")

@app.route("/api/system-info")
def system_info():
    """API Endpoint สำหรับดึงข้อมูลระบบด้วย Python JSON Response"""
    meta = get_system_metadata()
    return jsonify(meta)

if __name__ == "__main__":
    print("==================================================")
    print("  กำลังเริ่มทำงานระบบ Leave Management System...  ")
    print("  เปิดเบราว์เซอร์ไปที่: http://127.0.0.1:5000       ")
    print("==================================================")
    app.run(debug=True, port=5000)