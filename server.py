from flask import Flask
from routes.system import system_bp
from routes.exec import exec_bp
from routes.keyboard import keyboard_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(system_bp)
app.register_blueprint(exec_bp)
app.register_blueprint(keyboard_bp)

if __name__ == '__main__':
    # Running on 0.0.0.0 to be accessible from other machines
    app.run(host='0.0.0.0', port=5000)
