import paramiko

HOST = "ssh-chatbruti.alwaysdata.net"
USER = "chatbruti"
PASS = "qoDkag-huvxim-8qunwi"

def verify_index():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASS)
        
        print("Checking index.html for cache buster...")
        cmd = "grep 'favicon.png?v=2' ~/www/app/templates/index.html"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode().strip()
        
        if out:
            print("FOUND:", out)
        else:
            print("NOT FOUND")
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_index()
