import os
import time
import subprocess
from dotenv import load_dotenv

load_dotenv()

def tcp_parser():
    script_path = 'scripts/tcp.sh'

    PFSENSE_IPDARR = os.environ["PFSENSE_IPADDR"]
    PFSENSE_TCP_PORT = os.environ["PFSENSE_TCP_PORT"]

    # Execute the Bash script.
    try:
        subprocess.run(['bash', script_path], check=True)
        print("Bash script executed successfully.")
    except subprocess.CalledProcessError as e:
            # Check if the error message indicates missing environment variables
            error_message = str(e)
            if "No such file or directory" in error_message or "Error: PFSENSE_IPADDR or PFSENSE_TCP_PORT environment variables are not set." in error_message:
                print(f"Error executing Bash script: {error_message}")
                
                # Set environment variables
                commands = [f'export PFSENSE_IPADDR="{PFSENSE_IPDARR}"', f'export PFSENSE_TCP_PORT={int(PFSENSE_TCP_PORT)}']
                for bash_command in commands:
                    subprocess.run(['bash', '-c', bash_command], check=True, text=True, capture_output=True)
                print("Environment variables set.")
                time.sleep(1)
            else:
                raise