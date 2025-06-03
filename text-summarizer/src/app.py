from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from summarizer import TextSummarizer
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

summarizer = TextSummarizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data.get('text', '')
        num_sentences = int(data.get('num_sentences', 3))
        summary = summarizer.get_summary(text, num_sentences)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        summary = data.get('summary', '')
        if not summary:
            return jsonify({'error': 'No summary to download'}), 400
            
        # Use timestamp for filename
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.txt"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Create uploads directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(summary)
            
        # Instead of returning filename, serve the file directly
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)