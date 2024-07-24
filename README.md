# Mikrotik Router Configuration Script

This Python script helps with the configuration of Mikrotik routers, specifically designed for managing backups, user accounts, and firewall NAT rules. 

** I would say that this script is in the early beta stage, so please be careful. **

## Features

1. **Connect to the Router**: Verifies connection to the router via SSH.
2. **Backups**:
   - Create new backups.
   - List existing backups.
   - Download selected backups.
   - Delete backups with confirmation.
3. **User Management**:
   - List users with details.
   - Add new users.
   - Disable users.
   - Delete users with confirmation, ensuring at least one admin remains.
4. **Firewall NAT Rules**:
   - List all existing NAT rules in a table format.
   - Add new NAT rules with user confirmation before applying.
   - Remove NAT rules with user confirmation before deletion.

## TO-DO List

1. WiFi configuration
2. WireGuard configuration

## Requirements

- Python 3
- The following Python packages:
  - `paramiko`
  - `routeros_api`
  - `prettytable`

These packages can be installed using pip:

pip install paramiko routeros_api prettytable

Setup

	1.	Clone this repository to your local machine.
	2.	Enable SSH on your Mikrotik router and add the necessary firewall rules to allow connections.
	3.	Create a settings.conf file with the router’s IP and port (the password is not stored for security reasons). Example:

[router]
ip = 192.168.88.1

username = admin

port = 22

4. Run the script: python main.py

Usage

The script runs in a terminal window. After starting the script, you will see a menu with options for managing backups, users, and firewall NAT rules. Follow the prompts to perform the desired operations.

Note

	•	This script was created for my hAP ax3 router.
	•	The IP address and port of the router are stored in a configuration file, but the password is not stored anywhere for security reasons.
	•	Once the WiFi and WireGuard configuration options are ready, I plan to share the code on GitHub if anyone is interested.

Disclaimer

I don’t know how to program; this script was generated with ChatGPT. I am not responsible for its use or any errors it may cause.

Contributing

If you have any suggestions or ideas for additional features, improvements, or functionalities that would be helpful, please feel free to open an issue or submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.
