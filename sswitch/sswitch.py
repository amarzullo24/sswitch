#!/usr/bin/env python3
import re
import sys
import os
import configparser

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
    config_file = get_ssh_config_path()
    
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} HOST NEW_IP")
        sys.exit(1)
    
    host = sys.argv[1]
    new_ip = sys.argv[2]
    
    if not update_hostname(config_file, host, new_ip):
        sys.exit(1)

if __name__ == "__main__":
    main()
