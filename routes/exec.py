import subprocess
from flask import Blueprint, request, jsonify

exec_bp = Blueprint('exec', __name__)

@exec_bp.route('/exec', methods=['POST'])
def execute_script():
    try:
        data = request.get_json(force=True)
        script = data.get('script')
        if not script:
            return jsonify({"status": "error", "message": "No script provided"}), 400
        
        # Execute the script
        result = subprocess.run(script, shell=True, capture_output=True, text=True)
        
        return jsonify({
            "status": "success", 
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
