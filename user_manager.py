import os
import getpass
from prettytable import PrettyTable

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(message="Press any key to continue..."):
    input(message)

def manage_users(api):
    while True:
        clear_screen()
        print_users(api)
        
        print("\n1. List users")
        print("2. Add user")
        print("3. Disable user")
        print("4. Delete user")
        print("B. Back")

        choice = input("Enter your choice: ").strip().lower()
        clear_screen()
        if choice == '1':
            print_users(api)
            pause()
        elif choice == '2':
            add_user(api)
            pause()
        elif choice == '3':
            disable_user(api)
            pause()
        elif choice == '4':
            delete_user(api)
            pause()
        elif choice == 'b':
            break
        else:
            print("Invalid choice, please try again.")

def print_users(api):
    users = api.get_resource('/user').get()
    table = PrettyTable()
    table.field_names = ["Name", "Group", "Last logged in", "Comment"]
    
    for user in users:
        table.add_row([
            user['name'], 
            user['group'], 
            user.get('last-logged-in', 'N/A'), 
            user.get('comment', 'N/A')
        ])
    
    print(table)

def add_user(api):
    name = input("Enter the new user's name: ")
    password = getpass.getpass(f"Enter the password for {name}: ")
    group = input("Enter the group for the new user (default: read): ").strip() or 'read'
    comment = input("Enter a comment for the new user: ")

    api.get_resource('/user').add(name=name, password=password, group=group, comment=comment)
    print(f"User {name} added successfully.")

def disable_user(api):
    users = api.get_resource('/user').get()
    print("Select a user to disable:")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user['name']}")
    print("B. Back")

    choice = input("Enter your choice: ").strip().lower()
    if choice == 'b':
        return
    try:
        index = int(choice) - 1
        if 0 <= index < len(users):
            user_to_disable = users[index]
            api.get_resource('/user').set(id=user_to_disable['.id'], disabled='true')
            print(f"User {user_to_disable['name']} disabled successfully.")
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"Error disabling user: {e}")

def delete_user(api):
    users = api.get_resource('/user').get()
    if len(users) <= 1:
        print("Cannot delete the last remaining user.")
        pause()
        return

    print("Select a user to delete:")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user['name']}")
    print("B. Back")

    choice = input("Enter your choice: ").strip().lower()
    if choice == 'b':
        return
    try:
        index = int(choice) - 1
        if 0 <= index < len(users):
            user_to_delete = users[index]
            if 'full' in user_to_delete['group'] and sum(1 for user in users if 'full' in user['group']) == 1:
                print("Cannot delete the last remaining full user.")
                pause()
                return
            api.get_resource('/user').remove(id=user_to_delete['.id'])
            print(f"User {user_to_delete['name']} deleted successfully.")
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"Error deleting user: {e}")