from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    print("กำลังเริ่มทำงานระบบ Leave Management System...")
    print("เปิดเบราว์เซอร์ไปที่: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)