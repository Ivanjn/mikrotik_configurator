import os
import time
from datetime import datetime

ssh_client = None

def set_ssh_client(client):
    global ssh_client
    ssh_client = client

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(message="Press any key to continue..."):
    input(message)

def manage_backups(ssh_client):
    while True:
        clear_screen()
        print_backups()
        
        print("\n0. List backup files")
        print("1. Create new backup")
        print("2. Delete backups")
        print("3. Download backup")
        print("B. Back")

        choice = input("Enter your choice: ").strip().lower()
        clear_screen()
        if choice == '0':
            print_backups()
            pause()
        elif choice == '1':
            create_backup(ssh_client)
            pause()
        elif choice == '2':
            delete_backup(ssh_client)
            pause()
        elif choice == '3':
            download_backup(ssh_client)
            pause()
        elif choice == 'b':
            break
        else:
            print("Invalid choice, please try again.")

def print_backups():
    backups = list_backups()
    if backups:
        print("Existing backups:")
        for i, backup in enumerate(backups, 1):
            print(f"{i}. {backup}")
    else:
        print("No backups available.")

def create_backup(ssh_client):
    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    backup_name = f'{timestamp}.backup'
    command = f'/system backup save name={backup_name}'

    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        stdout.channel.recv_exit_status()  # Wait for command to complete
        print(f"Backup created successfully: {backup_name}")
        time.sleep(2)  # Add delay to ensure the backup is created before listing
        print_backups()  # Print the updated list of backups
    except Exception as e:
        print(f"Error creating backup: {e}")

def delete_backup(ssh_client):
    backups = list_backups()
    if not backups:
        print("No backups available to delete.")
        return

    print("Select a backup to delete:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")
    print("B. Back")

    choice = input("Enter your choice: ").strip().lower()
    if choice == 'b':
        return
    try:
        index = int(choice) - 1
        if 0 <= index < len(backups):
            backup_to_delete = backups[index]
            confirm = input(f"Are you sure you want to delete {backup_to_delete}? (y/n): ").strip().lower()
            if confirm == 'y':
                command = f'/file remove "{backup_to_delete}"'
                try:
                    stdin, stdout, stderr = ssh_client.exec_command(command)
                    stdout.channel.recv_exit_status()  # Wait for command to complete
                    print(f"Backup {backup_to_delete} deleted successfully.")
                except Exception as e:
                    print(f"Error deleting backup: {e}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice.")

def download_backup(ssh_client):
    backups = list_backups()
    if not backups:
        print("No backups available to download.")
        return

    print("Select a backup to download:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")
    print("B. Back")

    choice = input("Enter your choice: ").strip().lower()
    if choice == 'b':
        return
    try:
        index = int(choice) - 1
        if 0 <= index < len(backups):
            backup_to_download = backups[index]
            local_path = os.path.join('backups', backup_to_download)
            remote_path = f'/backup/{backup_to_download}'
            try:
                ftp_client = ssh_client.open_sftp()
                ftp_client.get(remote_path, local_path)
                ftp_client.close()
                print(f"Backup {backup_to_download} downloaded successfully: {local_path}")
            except Exception as e:
                print(f"Error downloading backup: {e}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice.")

def list_backups():
    try:
        command = '/file print where name~".backup"'
        stdin, stdout, stderr = ssh_client.exec_command(command)
        result = stdout.read().decode()
        lines = result.strip().split('\\n')[2:]  # Skip the header lines
        backups = [line.split()[1] for line in lines if '.backup' in line]
        return backups
    except Exception as e:
        print(f"Error listing backups: {e}")
        return []