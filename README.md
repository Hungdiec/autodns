# NPM Proxy & Cloudflare DNS Update Service

This project automates the process of updating Cloudflare DNS records based on proxy host changes from NPM (Nginx Proxy Manager). It uses a Python script to fetch proxy host information from NPM and then creates or deletes Cloudflare CNAME records accordingly. The script is installed as a systemd service that runs every 5 seconds.

## Features

- **Automated Updates:**  
  Automatically checks for changes in NPM proxy hosts and updates Cloudflare DNS records.
- **Systemd Integration:**  
  Runs as a systemd service with a timer that executes the update script every 5 seconds.
- **Interactive Installation:**  
  The installation script prompts for all necessary configuration values.
- **Easy Uninstallation:**  
  An uninstall script removes all generated files and disables the services.

## Directory Structure

```plaintext
npm-proxy-cloudflare/
├── listhostpython.py      # Main Python script (reads configuration from config.py)
├── install.sh             # Installer script for configuring and installing the service
├── uninstall.sh           # Uninstaller script to remove the service and configuration
└── README.md              # This documentation file
```
## Requirements
Ubuntu (or another systemd-enabled Linux distribution)
Python 3 and pip3
The Python requests library (installed via pip)

## Installation
You can install the project with one command by cloning the repository and running the installer script. For example:
```bash
curl -sSL https://github.com/yourusername/yourrepo/archive/refs/heads/main.tar.gz | tar -xz && cd yourrepo-main && ./install.sh
```
## What the Installer Does
- **Installs Dependencies**:
- **Updates the package list and installs Python3, pip3, and the requests library.**
- **Prompts for Configuration:**
- **Asks you for your NPM API URL, user, password, Cloudflare API token, Zone ID, and server IP/hostname.**
- **Creates Configuration File:**
- **Writes your configuration values to config.py.**
- **Sets Up Systemd Service and Timer:**
- **Creates and installs the systemd service (npm_proxy_update.service) and timer (npm_proxy_update.timer) files. The service runs the update script every 5 seconds.**
- **Enables and Starts the Timer:**
- **Reloads the systemd daemon, enables, and starts the timer so that the update process begins automatically.**

## Configuration
**During installation, you will be prompted for the following configuration values:**

- **NPM API URL:**
- **e.g., https://proxy.hung99.com/api**
- **NPM API User:**
- **Your NPM API username/email.**
- **NPM API Password:**
- **Your NPM API password.**
- **Cloudflare API Token:**
- **Your Cloudflare API token.**
- **Cloudflare Zone ID:**
- **Your Cloudflare zone ID.**
- **Server IP or Hostname:**
- **The IP or hostname to be used as the CNAME record content.**
- **These values are saved in the config.py file (generated during installation) and are used by listhostpython.py.**

## Running the Service
After installation, the systemd timer will automatically trigger the service every 5 seconds. To check the status of the timer or service, use the following commands:
```bash
# Check timer status
sudo systemctl status npm_proxy_update.timer

# Check service status (after a run)
sudo systemctl status npm_proxy_update.service

# View logs for the service
sudo journalctl -u npm_proxy_update.service -f
```
## Uninstallation
To uninstall the service and remove the generated configuration file, run the provided uninstaller:
```bash
sudo bash uninstall.sh
```
The uninstaller will:

Stop and disable the systemd timer and service.
Remove the systemd unit files from /etc/systemd/system/.
Reload the systemd daemon.
Remove the generated config.py file.
## License
Include your project's license information here.

## Contributing
If you want to contribute, please fork the repository and create a pull request with your improvements.
