import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request

# Ensure the root directory is in the path so imports work
sys.path.append(os.path.dirname(__file__))

app = Flask(__name__)

# Mock database for analysis results
RESULTS_FILE = os.path.join(os.path.dirname(__file__), 'analysis_results.json')

def load_results():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    return []

@app.route('/')
def index():
    results = load_results()
    return render_template('index.html', results=results)

@app.route('/run-analysis', methods=['POST'])
def run_analysis():
    try:
        from skills.analyze import run_orchestration
        run_orchestration()
        return jsonify({"status": "Analysis completed", "time": datetime.now().isoformat()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/results')
def get_results():
    return jsonify(load_results())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
