# app.py - ควบคุมการทำงานหลักด้วย Flask และ Python

from flask import Flask, render_template_string, jsonify
from utils import get_system_metadata
from template_code import HTML_TEMPLATE

app = Flask(__name__)

@app.route("/")
def index():
    meta = get_system_metadata()
    print(f"กำลังให้บริการ: {meta['system_name']}")
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/system-info")
def system_info():
    return jsonify(get_system_metadata())

if __name__ == "__main__":
    print("==================================================")
    print("  Leave Management System (100% Python Files)     ")
    print("  เปิดเบราว์เซอร์ไปที่: http://127.0.0.1:5000       ")
    print("==================================================")
    app.run(debug=True, port=5000)