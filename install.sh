#!/bin/bash

# Ensure script is run as root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root"
  exit 1
fi

echo "Installing System Control Server..."

# Install dependencies via apt (avoiding pip on externally managed environments)
apt-get update
apt-get install -y python3-flask

# Copy service file
cp system-control.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable and start service
systemctl enable system-control.service
systemctl restart system-control.service

echo "Service installed and started!"
systemctl status system-control.service
