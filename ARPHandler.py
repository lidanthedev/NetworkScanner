import threading
import logging

from scapy.sendrecv import srp, sr1, sr

from AttackHandler import AttackHandler
from PacketWrapper import ARPPacket, ARPReplyPacket, MACPacket
from scapy.layers.l2 import ARP, Ether


class ARPHandler(AttackHandler):
    arp_table: dict[str, str]

    def __init__(self):
        super().__init__(AttackHandler.ARP_HANDLER_ID)
        self.arp_table = {}

        # run find_device_on_network in a thread

        scanner_thread = threading.Thread(target=self.find_devices_on_network, daemon=True)
        scanner_thread.start()

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
                self.save_attack(arp_packet, False)


    def protect_attack(self):
        print("PROTECT ARP!!!!")

    def find_devices_on_network(self):
        scapy_logger = logging.getLogger("scapy.runtime")
        old_level = scapy_logger.level
        scapy_logger.setLevel(logging.ERROR)
        arp_request = ARP() / Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request.pdst = arp_request.psrc + "/24"
        sr(arp_request, timeout=1, verbose=False)
        scapy_logger.setLevel(old_level)
        print("ARP SCAN COMPLETE")
