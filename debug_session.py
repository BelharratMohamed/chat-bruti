import paramiko

HOST = "ssh-chatbruti.alwaysdata.net"
USER = "chatbruti"
PASS = "qoDkag-huvxim-8qunwi"

def debug_session():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASS)
        
        print("Checking flask_session directory...")
        stdin, stdout, stderr = ssh.exec_command("ls -la ~/www/flask_session")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("Checking logs for history endpoint...")
        # Grep for /history in logs
        cmd = "grep '/history' ~/admin/logs/http/*.log | tail -n 20"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_session()
