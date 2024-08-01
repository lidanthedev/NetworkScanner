import subprocess
import Logger


def get_current_ssid():
    """
    Get the current ssid
    :return:
    """
    try:
        result = subprocess.check_output(['iwgetid', '--raw'], stderr=subprocess.STDOUT, text=True)
        ssid = result.strip()
        return ssid
    except Exception as e:
        return "Ethernet"


def get_wifi_networks(min_frequency, max_frequency):
    """
    Get the Wi-Fi networks
    :param min_frequency: the minimum frequency
    :param max_frequency: the maximum frequency
    :return: the Wi-Fi networks
    """
    try:
        result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True)
        # print(result.stdout)
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
            Logger.log(f"Error in EvilTwin: {result.stderr} (Are you in Windows?)")
            return None

    except Exception as e:
        Logger.log(f"An error occurred with EvilTwin: {e} (Are you in Windows?)")
        return None


def disconnect_from_current_wifi(wifi_interface):
    """
    Will disconnect from the current wifi
    :param wifi_interface: the wifi interface to disconnect from
    :return: None
    """
    # Run nmcli command to disconnect from the current Wi-Fi network
    command = ["nmcli", "dev", "disconnect", wifi_interface]

    # Execute the command
    subprocess.run(command)


def connect_to_wifi(ssid):
    """
    Will connect to the given SSID
    :param ssid: the ssid to connect
    :return: None
    """
    # Use nmcli to connect to WiFi
    cmd = f"nmcli dev wifi connect '{ssid}'"

    try:
        subprocess.run(cmd, shell=True, check=True)
        Logger.log(f"Successfully connected to {ssid}")
    except subprocess.CalledProcessError as e:
        Logger.log(f"Failed to connect to {ssid}. Error: {e}")


def get_wifi_interface():
    """
    Will return the current wifi interface
    :return: the wifi-interface
    """
    try:
        cmd = "iwconfig 2>&1 | awk '/IEEE/{print $1}'"
        result = subprocess.check_output(cmd, shell=True, text=True).strip()
        return result
    except subprocess.CalledProcessError as e:
        Logger.log(f"Error: {e}")
        return None