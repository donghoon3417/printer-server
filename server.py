from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///printer_data.db'
db = SQLAlchemy(app)

class PrinterStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), nullable=False)
    page_count = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def home():
    return "<h2>프린터 상태 서버 실행 중</h2><p>/status/장비ID 예: /status/store001</p>"

@app.route("/status/<device_id>")
def status(device_id):
    record = PrinterStatus.query.filter_by(device_id=device_id).order_by(PrinterStatus.timestamp.desc()).first()
    if record:
        return jsonify({
            "device_id": record.device_id,
            "page_count": record.page_count,
            "timestamp": record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        return jsonify({"error": "해당 장비 ID의 데이터가 없습니다."}), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
