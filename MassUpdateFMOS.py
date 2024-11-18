import pexpect
import getpass
import sys
import os

def read_servers(filename):
    with open(filename, 'r') as f:
        servers = [line.strip() for line in f if line.strip()]
    return servers

def get_credentials():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    filename = input("Enter filename to transfer: ")
    # Check if the file exists locally
    if not os.path.isfile(filename):
        print(f"File '{filename}' does not exist.")
        sys.exit(1)
    return username, password, filename

def scp_file(server, username, password, filename):
    scp_command = f"scp {filename} {username}@{server}:/var/tmp/"
    print(f"Running command: {scp_command}")
    child = pexpect.spawn(scp_command)
    scp_expect_list = [
        'Are you sure you want to continue connecting',
        '[Pp]assword:',
        'Permission denied',
        'No such file or directory',
        'scp:.*',
        '100%',
        pexpect.EOF,
        pexpect.TIMEOUT,
    ]
    while True:
        try:
            i = child.expect(scp_expect_list, timeout=60)
        except pexpect.EOF:
            break
        except pexpect.TIMEOUT:
            print(f"SCP to {server} timed out")
            return False

        if i == 0:
            # Are you sure you want to continue connecting
            child.sendline('yes')
        elif i == 1:
            # Password prompt
            child.sendline(password)
        elif i == 2:
            print(f"Permission denied when connecting to {server}")
            return False
        elif i == 3:
            print(f"No such file or directory: {filename}")
            return False
        elif i == 4:
            # scp error
            print(f"SCP error: {child.after.decode('utf-8', 'ignore')}")
            return False
        elif i == 5:
            # File transfer progress, 100%
            # Wait for EOF
            child.expect(pexpect.EOF)
            break
        elif i == 6:
            # EOF
            break
        elif i == 7:
            # TIMEOUT
            print(f"SCP to {server} timed out")
            return False
    return True

def ssh_and_run_command(server, username, password, filename):
    ssh_command = f"ssh {username}@{server}"
    print(f"Running command: {ssh_command}")
    child = pexpect.spawn(ssh_command)
    ssh_expect_list = [
        'Are you sure you want to continue connecting',
        '[Pp]assword:',
        'This is FMOS .*',
        'Enter one now',
        'Remind me later',
        'Select an option:',
        '[#\$] ',  # shell prompt
        pexpect.EOF,
        pexpect.TIMEOUT,
    ]
    while True:
        try:
            i = child.expect(ssh_expect_list, timeout=60)
        except pexpect.EOF:
            print(f"SSH session to {server} ended unexpectedly")
            return False
        except pexpect.TIMEOUT:
            print(f"SSH to {server} timed out")
            return False

        if i == 0:
            # Are you sure you want to continue connecting
            child.sendline('yes')
        elif i == 1:
            # Password prompt
            child.sendline(password)
        elif i == 2:
            # 'This is FMOS .*'
            continue  # Read next prompt
        elif i == 3 or i == 4 or i == 5:
            # 'Enter one now' or 'Remind me later' or 'Select an option:'
            # Send '2' to select 'Remind me later'
            child.sendline('2')
        elif i == 6:
            # Got shell prompt
            break
        elif i == 7:
            # EOF
            print(f"SSH session to {server} ended unexpectedly")
            return False
        elif i == 8:
            # TIMEOUT
            print(f"SSH to {server} timed out")
            return False
    # Now at shell prompt, send the command
    child.sendline(f'fmos update /var/tmp/{os.path.basename(filename)}')
    # Wait for the command to complete or for the prompt to reappear
    try:
        child.expect('[#\$] ', timeout=300)
    except pexpect.TIMEOUT:
        print(f"Command on {server} timed out")
        return False
    # Exit SSH session
    child.sendline('exit')
    child.expect(pexpect.EOF)
    return True

def main():
    servers = read_servers('servers.txt')
    username, password, filename = get_credentials()
    for server in servers:
        print(f"\nProcessing server: {server}")
        success = scp_file(server, username, password, filename)
        if not success:
            print(f"Failed to transfer file to {server}")
            continue
        success = ssh_and_run_command(server, username, password, filename)
        if not success:
            print(f"Failed to run command on {server}")
            continue
        print(f"Finished processing server: {server}")

if __name__ == '__main__':
    main()
