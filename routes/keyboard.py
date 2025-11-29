import os
import re
import subprocess
from flask import Blueprint, jsonify

keyboard_bp = Blueprint('keyboard', __name__)

def get_x11_env():
    """Helper to get X11 environment variables."""
    # Common Xauthority paths
    xauth_paths = [
        '/run/user/1000/gdm/Xauthority',
        '/home/rajesh/.Xauthority',
        '/run/user/1000/xauth_monitor'
    ]
    
    xauth = None
    for path in xauth_paths:
        if os.path.exists(path):
            xauth = path
            break
            
    env = os.environ.copy()
    if xauth:
        env['XAUTHORITY'] = xauth
    
    return env

def get_xinput_list(env):
    """Run xinput list and return output if successful on any display."""
    displays = [':0', ':1']
    last_error = None
    
    for display in displays:
        try:
            current_env = env.copy()
            current_env['DISPLAY'] = display
            # Run xinput list directly to avoid shell pipe masking exit codes
            result = subprocess.run(['xinput', 'list'], capture_output=True, text=True, env=current_env)
            
            if result.returncode == 0:
                return result.stdout, display
            else:
                # If it failed, it's likely a display issue. Log/store error and try next.
                last_error = result.stderr
                continue
        except Exception as e:
            last_error = str(e)
            continue
            
    raise Exception(f"Failed to run xinput list on any display. Last error: {last_error}")

@keyboard_bp.route('/keyboardstatus', methods=['GET', 'POST'])
def keyboard_status():
    try:
        env = get_x11_env()
        full_list, _ = get_xinput_list(env)
        
        # Filter for "Asus Keyboard"
        output_lines = []
        for line in full_list.splitlines():
            if "Asus Keyboard" in line:
                output_lines.append(line)
        
        output = "\n".join(output_lines)
        if output:
            output += "\n" # Add trailing newline to match grep behavior roughly
            
        return jsonify({"status": "success", "output": output}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@keyboard_bp.route('/keyboarddisableinternal', methods=['GET', 'POST'])
def keyboard_disable_internal():
    try:
        env = get_x11_env()
        
        # Step 1: Get list and active display
        try:
            full_list, active_display = get_xinput_list(env)
        except Exception as e:
             return jsonify({"status": "error", "message": str(e)}), 500
            
        final_env = env.copy()
        final_env['DISPLAY'] = active_display

        # Step 2: Extract IDs from "Asus Keyboard" lines
        # Format: "∼ Asus Keyboard id=13 [floating slave]"
        ids = []
        for line in full_list.splitlines():
            if "Asus Keyboard" in line:
                match = re.search(r'id=(\d+)', line)
                if match:
                    ids.append(match.group(1))
        
        # Step 3: Float each ID
        for dev_id in ids:
            cmd_float = ['xinput', 'float', dev_id]
            subprocess.run(cmd_float, check=True, env=final_env)
            
        # Step 4: Get list again to return status
        # We assume the same display still works
        result_final = subprocess.run(['xinput', 'list'], capture_output=True, text=True, env=final_env)
        
        # Filter final output
        final_output_lines = []
        for line in result_final.stdout.splitlines():
             if "Asus Keyboard" in line:
                final_output_lines.append(line)
        
        final_output = "\n".join(final_output_lines)
        if final_output:
            final_output += "\n"

        return jsonify({
            "status": "success", 
            "disabled_ids": ids,
            "final_output": final_output
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
