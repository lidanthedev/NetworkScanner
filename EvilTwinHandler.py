import collections
import subprocess
import time

from AttackHandler import AttackHandler


class EvilTwinHandler(AttackHandler):
    TIME_TO_CHECK_EVILTWIN = 20

    def __init__(self):
        self.time_since_last_check = time.perf_counter()

    def handle_packet(self, better_packet):

        # we don't want to check for each packet, that would be a waste
        if time.perf_counter() - self.time_since_last_check > self.TIME_TO_CHECK_EVILTWIN:
            self.time_since_last_check = time.perf_counter()

            current_networks = self.get_wifi_networks()
            # get all networks that appear with the same name more than once
            duplicates = [item for item, count in collections.Counter(current_networks).items() if count > 1]
            if "" in duplicates:
                duplicates.remove("")

            if len(duplicates) > 0:
                print(f"Evil Twin Detected, networks that appear more than once:")
                for network in duplicates:
                    print(f"\t{network}")

    def protect_attack(self):
        pass

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
