from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
from analyze_radio_schedule import extract_data_from_docx, analyze

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp:
        file.save(temp.name)
        try:
            rows = extract_data_from_docx(temp.name)
            result = analyze(rows)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            os.unlink(temp.name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)