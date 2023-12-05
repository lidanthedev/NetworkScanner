from AttackHandler import AttackHandler
from PacketWrapper import ARPPacket, ARPReplyPacket, MACPacket
from scapy.layers.l2 import ARP, Ether


class ARPHandler(AttackHandler):
    arp_table: dict[str, str]

    def __init__(self):
        self.arp_table = {}
        self.find_devices_on_network()

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
    
    def find_devices_on_network(self):
        # using scapy send arp request to all ips on network
        # if response is received then add to arp table
        arp_request = ARP(pdst="192.168.1.0/24") / Ether(dst="ff:ff:ff:ff:ff:ff")
        my_ip = arp_request[ARP].psrc
        self.find_device_on_network()
        
    
    def find_device_on_network(self, my_ip, last_digit: int):
        
        ip_split = my_ip.split(".")
        ip_split[3] = str(last_digit)
        broadcast_ip = ".".join(ip_split)
        
        arp_request[ARP].pdst = broadcast_ip
        ARP_request_broadcast = broadcast/ARP_request
        answered_list = srp(ARP_request_broadcast, timeout=1, verbose=False)[0]

        for element in answered_list:
            self.arp_table[element[1].psrc] = element[1].hwsrc
            print("IP: " + element[1].psrc + " MAC: " + element[1].hwsrc)
        