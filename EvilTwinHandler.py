import collections
import subprocess

from AttackHandler import AttackHandler

class EvilTwinHandler(AttackHandler):
    def __init__(self):
        self.mac_table = {}

    def handle_packet(self, better_packet):
        current_networks = self.get_wifi_networks()
        duplicates = [item for item, count in collections.Counter(current_networks).items() if count > 1]
        if "" in duplicates:
            duplicates.remove("")

        if len(duplicates) > 0:
            print(f"Evil Twin Detected, networks that appear more than once:")
            for network in duplicates:
                print(f"\t{network}")

    def get_wifi_networks(self):
        try:
            result = subprocess.check_output(['iwlist', 'scan'], stderr=subprocess.STDOUT, text=True)

            if result.returncode == 0:
                networks = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'ESSID' in line]
                return networks
            else:
                print(f"Error: {result.stderr}")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
