# Ubuntu System Control Server

A Flask-based application that runs as a systemd background service on Ubuntu.

## Setup

1.  **Clone the repository** (if you haven't already).
2.  **Run the installation script** as root:
    ```bash
    sudo ./install.sh
    ```
    This script will:
    - Install Python dependencies (`flask`).
    - Install the systemd service (`system-control.service`).
    - Enable and start the service.

## API Endpoints

The server runs on port `5000` by default.

### System Control

#### 1. Ping
Check if the server is online.
- **URL**: `/ping`
- **Method**: `GET`
- **Example**:
  ```bash
  curl http://localhost:5000/ping
  ```

#### 2. Sleep
Put the computer to sleep (suspend).
- **URL**: `/sleep`
- **Method**: `POST`
- **Example**:
  ```bash
  curl -X POST http://localhost:5000/sleep
  ```

#### 3. Screen Off
Turn off the screen (supports X11).
- **URL**: `/screenoff`
- **Method**: `POST`
- **Example**:
  ```bash
  curl -X POST http://localhost:5000/screenoff
  ```

### Execution

#### 4. Execute Script
Execute a custom shell command or script.
- **URL**: `/exec`
- **Method**: `POST`
- **Body**: JSON `{"script": "command_to_run"}`
- **Example**:
  ```bash
  curl -X POST http://localhost:5000/exec -d '{"script": "echo Hello World"}'
  ```
  > **Warning**: This endpoint allows arbitrary command execution as root. Ensure the server is secured.

### Keyboard Control (Asus)

#### 5. Keyboard Status
Get the status of the "Asus Keyboard" device from `xinput`.
- **URL**: `/keyboardstatus`
- **Method**: `GET`
- **Example**:
  ```bash
  curl http://localhost:5000/keyboardstatus
  ```

#### 6. Disable Internal Keyboard
Disables the internal Asus keyboard by floating the xinput device.
- **URL**: `/keyboarddisableinternal`
- **Method**: `GET`
- **Example**:
  ```bash
  curl http://localhost:5000/keyboarddisableinternal
  ```
