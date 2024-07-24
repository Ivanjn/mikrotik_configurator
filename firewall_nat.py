import os
from prettytable import PrettyTable

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(message="Press any key to continue..."):
    input(message)

def show_firewall_rules(api):
    rules = api.get_resource('/ip/firewall/nat').get()
    table = PrettyTable()
    table.field_names = ["#", "Comment", "Action", "Chain", "Src. Addr", "Dst. Addr", "Protocol", "Dst. Port"]
    for i, rule in enumerate(rules, 1):
        table.add_row([
            i,
            rule.get('comment', ''),
            rule.get('action', ''),
            rule.get('chain', ''),
            rule.get('src-address', ''),
            rule.get('to-addresses', ''),
            rule.get('protocol', ''),
            rule.get('dst-port', '')
        ])
    print(table)

def add_firewall_nat_rule(api):
    show_firewall_rules(api)
    
    add_rule = input("Do you want to add a new rule? (y/n): ").strip().lower()
    if add_rule != 'y':
        return

    ip = input("Enter the destination IP: ")
    port_range = input("Enter the port or port range (e.g., 16881-16885): ")
    print("Select the protocol:")
    print("1. TCP")
    print("2. UDP")
    print("3. Both")
    protocol_choice = input("Enter your choice (1/2/3): ").strip()
    
    if protocol_choice == '1':
        protocols = ['tcp']
    elif protocol_choice == '2':
        protocols = ['udp']
    elif protocol_choice == '3':
        protocols = ['tcp', 'udp']
    else:
        print("Invalid choice. Operation cancelled.")
        pause()
        return

    print("\nThe following rules will be created:")
    for proto in protocols:
        print(f"Firewall NAT rule: IP={ip}, Port={port_range}, Protocol={proto.upper()}")

    confirm = input("\nDo you want to apply these changes? (y/n): ").strip().lower()
    if confirm == 'y':
        for proto in protocols:
            # Create NAT rule
            api.get_resource('/ip/firewall/nat').add(
                chain="dstnat",
                action="dst-nat",
                to_addresses=ip,
                protocol=proto,
                dst_port=port_range
            )
            # Create firewall filter rule
            api.get_resource('/ip/firewall/filter').add(
                chain="forward",
                action="accept",
                protocol=proto,
                dst_address=ip,
                dst_port=port_range
            )
        print("Rules added successfully.")
    else:
        print("Operation cancelled.")

    pause()

def remove_firewall_nat_rule(api):
    show_firewall_rules(api)

    choice = input("Enter the number of the rule to delete: ").strip()
    try:
        index = int(choice) - 1
        rules = api.get_resource('/ip/firewall/nat').get()
        if 0 <= index < len(rules):
            rule_to_delete = rules[index]
            confirm = input(f"Are you sure you want to delete rule #{choice}? (y/n): ").strip().lower()
            if confirm == 'y':
                api.get_resource('/ip/firewall/nat').remove(id=rule_to_delete['.id'])
                print(f"Rule #{choice} deleted successfully.")
            else:
                print("Operation cancelled.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice.")

    pause()