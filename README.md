**Instructions to Use the Script:**

1. **Install Required Modules:**
   Make sure you have `pexpect` installed. You can install it using:
   ```bash
   pip install pexpect
   ```

2. **Create `servers.txt`:**
   Create a file named `servers.txt` in the same directory as your script. List one server per line.

3. **Place the Script in the Same Directory as the File to Transfer:**
   Ensure the script and the file you want to transfer are in the same directory, or provide the correct path to the file when prompted.

4. **Run the Script:**
   Execute the script using Python 3:
   ```bash
   python3 MassUpdateFMOS.py
   ```

5. **Provide the Necessary Inputs When Prompted:**
   - **Username:** Enter the username that exists on all servers.
   - **Password:** Enter the password associated with the username.
   - **Filename:** Enter the name of the file you wish to transfer.

**Script Behavior:**

- The script reads the list of servers from `servers.txt`.
- It prompts for the username, password, and the filename to transfer.
- For each server:
  - It uses `scp` to transfer the file to `/var/tmp/` on the server.
  - It handles SSH key verification prompts and password prompts.
  - It then SSHs into the server, handles any interactive prompts (such as entering '2' at the "Select an option:" prompt), and runs the `fmos update /var/tmp/filename` command.
  - It exits the SSH session after running the command.

**Notes:**

- **Error Handling:** The script includes basic error handling for common issues like timeouts and permission denials.
- **Interactive Prompts:** It uses `pexpect` to handle interactive prompts automatically.
- **Security:** Be cautious when handling passwords in scripts. Ensure that the script's permissions are secure and that you are complying with your organization's security policies.

**Dependencies:**

- Python 3.x
- `pexpect` library

**Disclaimer:**

- Ensure you have the necessary permissions to access the servers and run commands.
