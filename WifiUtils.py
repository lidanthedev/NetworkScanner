import subprocess


def get_current_ssid():
    try:
        result = subprocess.check_output(['iwgetid', '--raw'], stderr=subprocess.STDOUT, text=True)
        ssid = result.strip()
        return ssid
    except Exception as e:
        return "Ethernet"


def get_wifi_networks(min_frequency, max_frequency):
    try:
        result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            networks = []

            essid = ""
            frequency = 0
            for network in result.stdout.split('Address'):
                for line in network.split("\n"):
                    if 'ESSID' in line:
                        essid = line.split(':')[1].strip()
                    if 'Frequency' in line:
                        frequency = float(line.split(":")[1].split(" ")[0])

                if essid != "" and frequency != 0:
                    if min_frequency <= frequency <= max_frequency:
                        networks.append(essid)

            return networks
        else:
            print(f"Error in EvilTwin: {result.stderr} (Are you in Windows?)")
            return None

    except Exception as e:
        print(f"An error occurred with EvilTwin: {e} (Are you in Windows?)")
        return None
