import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

import chatbot

if not os.path.exists('logs'):
    os.makedirs('logs')
log_filename = os.path.join('logs', f'server_{datetime.now().strftime("%Y%m%d")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def handle_chat():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200


    if request.method == 'POST':
        try:
            data = request.json
            if not data or 'question' not in data:
                logger.warning("Yêu cầu không hợp lệ.")
                return jsonify({"text": "Yêu cầu không hợp lệ.", "videos": []}), 400

            question = data.get('question', '').strip()
            if not question:
                return jsonify({"text": "Vui lòng nhập câu hỏi.", "videos": []})
            
            logger.info(f"Nhận được câu hỏi từ client: '{question}'")
            response_data = chatbot.process_question(question)
            return jsonify(response_data)

        except Exception as e:
            logger.error(f"Lỗi xử lý yêu cầu: {e}", exc_info=True)
            return jsonify({"text": "Lỗi phía máy chủ.", "videos": []}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("=" * 60)
    print("     CHATBOT SERVER TƯ VẤN NGHIỆP VỤ Code PTIT     ")
    print("=" * 60)
    print(f"Server đang chạy tại: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)