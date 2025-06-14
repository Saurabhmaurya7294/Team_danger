from flask import Flask, request, jsonify, send_from_directory
from pinata_helper import upload_to_pinata
import os

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        ipfs_response = upload_to_pinata(filepath)
        print("IPFS Response:", ipfs_response)  # 👈 Add this line
        return jsonify(ipfs_response)
    return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(debug=True)