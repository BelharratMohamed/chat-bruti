import paramiko

HOST = "ssh-chatbruti.alwaysdata.net"
USER = "chatbruti"
PASS = "qoDkag-huvxim-8qunwi"

def copy_favicon_root():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASS)
        
        print("Copying favicon.png to favicon.ico in root...")
        # Copy and rename to .ico (browsers usually handle pngs named .ico fine these days)
        cmd = "cp ~/www/app/static/favicon.png ~/www/favicon.ico"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Also ensure static file serving for favicon.ico is handled if needed, 
        # but usually placing it in www/ works if the server serves static files from there.
        # However, since we are using WSGI, we might need to add a route for it if it's not served by Nginx/Apache before hitting Flask.
        # But let's try placing it there first.
        
        ssh.close()
        print("Favicon copied to root.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    copy_favicon_root()
