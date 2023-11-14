from AttackHandler import AttackHandler
import subprocess
from scapy.layers.dhcp import DHCP


class DHCPHandler(AttackHandler):
    def __init__(self):
        self.mac_table = {}

    def handle_packet(self, better_packet):

        if DHCP not in better_packet.packet:
            return

        # if joined a new network
        if self.is_packet_dhcp_ack(better_packet):

            # save the mac address of the joined network if it's the first time joining it
            network_name = self.get_current_ssid()
            if network_name not in self.mac_table:
                self.mac_table[network_name] = better_packet.get_source_mac()





        self.detect_attack(better_packet)

    def detect_attack(self, better_packet):
        if self.is_packet_dhcp_ack(better_packet):
            self.mac_table[better_packet.get_source_mac()] = self.get_current_ssid()

    def protect_attack(self):
        pass



    def is_packet_dhcp_ack(self, better_packet):
        return better_packet.packet[DHCP].options[0][1] == 5

    def get_current_ssid(self):
        # Run the 'iwgetid' command to get information about the current Wi-Fi connection
        result = subprocess.check_output(['iwgetid', '--raw'], stderr=subprocess.STDOUT, text=True)

        # Extract and return the SSID from the command output
        ssid = result.strip()
        return ssid