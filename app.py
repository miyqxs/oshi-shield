from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

def load_data():
    try:
        with open('data/chat_log.json', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/messages')
def messages():
    data = load_data()
    # Send last 100 messages, newest first
    return jsonify(data[-100:][::-1])

@app.route('/api/stats')
def stats():
    data = load_data()
    flagged = [m for m in data if m['flagged']]
    return jsonify({
        'total': len(data),
        'flagged': len(flagged),
        'clean': len(data) - len(flagged),
        'streams': len(set(m['video_id'] for m in data))
    })

if __name__ == '__main__':
    app.run(debug=True)