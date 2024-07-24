import subprocess
import sys
import configparser
import os
import getpass
import logging

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_packages():
    packages = ["paramiko", "routeros_api", "prettytable"]
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} not found. Installing...")
            install(package)

# Check and install required packages
check_and_install_packages()

# Now import the required modules
import paramiko
import routeros_api
from backup_manager import manage_backups, set_ssh_client
from user_manager import manage_users
from firewall_nat import add_firewall_nat_rule, remove_firewall_nat_rule

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(message="Press any key to continue..."):
    input(message)

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main_menu(ssh_client, api):
    set_ssh_client(ssh_client)
    while True:
        clear_screen()
        print("1. Backups")
        print("2. User Management")
        print("3. Add rule to firewall (NAT)")
        print("4. Remove rule from firewall (NAT)")
        print("Q. Quit")
        choice = input("Enter your choice: ").strip().lower()

        if choice == '1':
            clear_screen()
            manage_backups(ssh_client)
        elif choice == '2':
            clear_screen()
            manage_users(api)
        elif choice == '3':
            clear_screen()
            add_firewall_nat_rule(api)
        elif choice == '4':
            clear_screen()
            remove_firewall_nat_rule(api)
        elif choice == 'q':
            print("Goodbye!")
            ssh_client.close()
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    setup_logging()
    logging.info("Application started")

    # Load settings from settings.conf
    config = configparser.ConfigParser()
    config.read('settings.conf')
    ip = config.get('router', 'ip')
    username = config.get('router', 'username')
    port = config.get('router', 'port', fallback='22')
    password = config.get('router', 'password', fallback=None)

    if not password:
        password = getpass.getpass(f"Enter the password for {username}@{ip}: ")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Trying to connect using IP: {ip} and User: {username}")
        ssh_client.connect(ip, username=username, password=password, port=int(port))
        
        # Establish RouterOS API connection
        connection = routeros_api.RouterOsApiPool(ip, username=username, password=password, plaintext_login=True)
        api = connection.get_api()
        
        clear_screen()
        main_menu(ssh_client, api)
    except Exception as e:
        logging.error(f"Connection error: {e}")
        print(f"Connection error: {e}")