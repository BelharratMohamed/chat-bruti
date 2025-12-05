import paramiko

HOST = "ssh-chatbruti.alwaysdata.net"
USER = "chatbruti"
PASS = "qoDkag-huvxim-8qunwi"

def verify_favicon():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASS)
        
        print("Checking for favicon.png...")
        stdin, stdout, stderr = ssh.exec_command("ls -l ~/www/app/static/favicon.png")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_favicon()
