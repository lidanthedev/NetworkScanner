from AttackHandler import AttackHandler
from scapy.layers.dhcp import DHCP


class DHCPHandler(AttackHandler):
    def __init__(self):
        self.mac_table = {}

    def handle_packet(self, better_packet):

        if DHCP not in better_packet.packet:
            return

        self.detect_attack(better_packet)

    def detect_attack(self, better_packet):
        if self.is_packet_dhcp_ack(better_packet):
            dns_domain = self.extract_dns_domain(better_packet)
            self.mac_table[better_packet.get_source_mac()] = dns_domain

    def protect_attack(self):
        pass



    def is_packet_dhcp_ack(self, better_packet):
        return better_packet.packet[DHCP].options[0][1] == 5

    def extract_dns_domain(self, better_packet):
        dns_domain = None
        if DHCP in better_packet.packet:
            dhcp_options = better_packet.packet[DHCP].options
            for option_code, option_data in dhcp_options:
                if option_code == 15:  # Option 15 corresponds to DNS Domain Name
                    dns_domain = option_data.decode('utf-8')
        return dns_domain
