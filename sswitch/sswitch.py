#!/usr/bin/env python3
import re
import sys
import os
import configparser
import argparse

# Default paths
DEFAULT_SSH_CONFIG = os.path.expanduser("~/.ssh/config")
CONFIG_FILE = os.path.expanduser("sswitch_config")

def get_ssh_config_path():
    """Retrieve the SSH config file location from the user's config file."""
    if os.path.isfile(CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return config.get("settings", "ssh_config", fallback=DEFAULT_SSH_CONFIG)
    return DEFAULT_SSH_CONFIG

def list_hostname(config_file):
    """List all HostNames from the SSH config file."""
    if not os.path.isfile(config_file):
        print(f"Error: Config file {config_file} not found!")
        return False

    with open(config_file, 'r') as f:
        lines = f.readlines()

    hostnames = []
    current_host = None

    for line in lines:
        host_match = re.match(r'^\s*Host\s+(.+)', line, re.IGNORECASE)
        if host_match:
            current_host = host_match.group(1)
        hostname_match = re.match(r'^\s*HostName\s+(.+)', line, re.IGNORECASE)
        if hostname_match and current_host:
            hostnames.append(f"{current_host} -> {hostname_match.group(1)}")

    if not hostnames:
        print("No hostnames found in the SSH config file.")
    else:
        print("Configured Hosts:")
        for entry in hostnames:
            print(entry)

    return True

def update_hostname(config_file, host, new_ip):
    """Update the SSH config file to change the HostName for a given host."""
    if not os.path.isfile(config_file):
        print(f"Error: Config file {config_file} not found!")
        return False

    with open(config_file, 'r') as f:
        lines = f.readlines()

    host_found = False
    in_target_host_block = False
    modified_lines = []

    for line in lines:
        if re.match(r'^\s*Host\s+', line, re.IGNORECASE):
            if re.match(r'^\s*Host\s+' + re.escape(host) + r'\s*$', line, re.IGNORECASE):
                in_target_host_block = True
                host_found = True
            else:
                in_target_host_block = False
        
        if in_target_host_block and re.match(r'^\s*HostName\s+', line, re.IGNORECASE):
            modified_line = re.sub(r'(^\s*HostName\s+).*', r'\g<1>' + new_ip, line)
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    if not host_found:
        print(f"Error: Host '{host}' not found in config file!")
        return False

    with open(config_file, 'w') as f:
        f.writelines(modified_lines)

    print(f"Successfully updated HostName for '{host}' to '{new_ip}' in {config_file}")
    return True

def main():
    """Main function to handle command-line arguments using argparse."""
    parser = argparse.ArgumentParser(description="Manage SSH HostName entries in the SSH config file.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List hostnames command
    subparsers.add_parser("list", help="List all configured SSH hosts")

    # Update hostname command
    update_parser = subparsers.add_parser("update", help="Update the HostName of a given SSH host")
    update_parser.add_argument("host", help="The SSH host to update")
    update_parser.add_argument("new_ip", help="The new IP address or hostname to set")

    args = parser.parse_args()
    config_file = get_ssh_config_path()

    if args.command == "list":
        list_hostname(config_file)
    elif args.command == "update":
        update_hostname(config_file, args.host, args.new_ip)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()