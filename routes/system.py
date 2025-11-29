import os
import subprocess
from flask import Blueprint, jsonify

system_bp = Blueprint('system', __name__)

@system_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "success", "message": "pong"}), 200

@system_bp.route('/sleep', methods=['GET', 'POST'])
def sleep():
    try:
        # Using systemctl suspend to put the computer to sleep
        subprocess.run(['systemctl', 'suspend'], check=True)
        return jsonify({"status": "success", "message": "System suspending..."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@system_bp.route('/screenoff', methods=['GET', 'POST'])
def screenoff():
    try:
        # Using xset to turn off the screen. 
        # Note: This requires the DISPLAY environment variable to be set correctly if running as a service.
        # We also need XAUTHORITY.
        
        # Common Xauthority paths for user 1000 (rajesh)
        xauth_paths = [
            '/run/user/1000/gdm/Xauthority',
            '/home/rajesh/.Xauthority',
            '/run/user/1000/xauth_monitor' # sometimes seen
        ]
        
        # Find Xauthority
        xauth = None
        for path in xauth_paths:
            if os.path.exists(path):
                xauth = path
                break
        
        # Try common displays
        displays = [':0', ':1']
        success = False
        last_error = None
        
        for display in displays:
            try:
                env = os.environ.copy()
                env['DISPLAY'] = display
                if xauth:
                    env['XAUTHORITY'] = xauth
                
                # Method 1: xset (X11)
                subprocess.run(['xset', 'dpms', 'force', 'off'], check=True, env=env)
                success = True
                break
            except Exception as e:
                last_error = e
                continue
        
        if not success:
            raise last_error or Exception("Failed to turn off screen on any display")
        
        return jsonify({"status": "success", "message": "Screen turned off"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
