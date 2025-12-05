import paramiko

HOST = "ssh-chatbruti.alwaysdata.net"
USER = "chatbruti"
PASS = "qoDkag-huvxim-8qunwi"

def check_logs():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASS)
        
        print("Checking HTTP error logs...")
        # Alwaysdata logs are typically in ~/admin/logs/http/
        # We'll look for the most recent error log file
        cmd = "ls -t ~/admin/logs/http/ | head -n 1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        latest_log = stdout.read().decode().strip()
        
        if latest_log:
            print(f"Reading tail of {latest_log}...")
            cmd = f"tail -n 50 ~/admin/logs/http/{latest_log}"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
        else:
            print("No logs found in ~/admin/logs/http/")
            
        # Also check if there's a specific app log if configured, but usually stderr goes to the http log
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_logs()
