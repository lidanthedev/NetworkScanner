import subprocess


def get_current_ssid():
    try:
        result = subprocess.check_output(['iwgetid', '--raw'], stderr=subprocess.STDOUT, text=True)
        ssid = result.strip()
        return ssid
    except Exception as e:
        return "Ethernet"


def get_wifi_networks():
    try:
        result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True)

        if result.returncode == 0:
            networks = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'ESSID' in line]
            return networks
        else:
            print(f"Error in EvilTwin: {result.stderr} (Are you in Windows?)")
            return None

    except Exception as e:
        print(f"An error occurred with EvilTwin: {e} (Are you in Windows?)")
        return None

