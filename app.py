import sys
# Ensure the root directory is in the path so imports work
sys.path.append(os.path.dirname(__file__))
import os
import subprocess
import json
from datetime import datetime

app = Flask(__name__)

# Mock database for analysis results
RESULTS_FILE = os.path.join(os.path.dirname(__file__), 'analysis_results.json')

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    return render_template('index.html', results=load_results())

@app.route('/run-analysis', methods=['POST'])
def run_analysis():
    # This triggers the /analyze skill logic
    try:
        from skills.analyze import run_orchestration
        # Run it synchronously for now to ensure it completes and writes the file
        run_orchestration()
        return jsonify({"status": "Analysis completed", "time": datetime.now().isoformat()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/results')
def get_results():
    return jsonify(load_results())

if __name__ == '__main__':
    app.run(port=5001, debug=True)
