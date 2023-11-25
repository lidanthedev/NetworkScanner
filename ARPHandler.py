from AttackHandler import AttackHandler
from PacketWrapper import ARPPacket, ARPReplyPacket, MACPacket


class ARPHandler(AttackHandler):
    arp_table: dict[str, str]

    def __init__(self):
        self.arp_table = {}

    def handle_packet(self, better_packet: MACPacket):
        if isinstance(better_packet, ARPPacket):
            self.handle_arp(better_packet)

    def handle_arp(self, arp_packet):
        if isinstance(arp_packet, ARPReplyPacket):
            ip = arp_packet.get_source_ip()
            if ip not in self.arp_table:
                self.arp_table[ip] = arp_packet.get_response_mac()
                print(f"ADD ARP ENTRY: IP {ip} has MAC address {self.arp_table[ip]}")
            elif arp_packet.get_response_mac() != self.arp_table[ip]:
                print(
                    f"DETECTED ARP POISONING: IP {ip} has multiple MAC addresses: {self.arp_table[ip]} and {arp_packet.get_response_mac()}"
                )

    def protect_attack(self):
        print("PROTECT ARP!!!!")