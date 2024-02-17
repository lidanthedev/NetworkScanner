import logging
import threading

from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import sr

import ArpUtils
import Logger
from AttackHandler import AttackHandler
from PacketWrapper import ARPPacket, ARPReplyPacket, MACPacket


def find_devices_on_network():
    """
    Scan devices on the network using ARP
    Uses a weird feature in scapy that allows you to send an ARP request to a broadcast MAC address to find all devices on the network
    """
    scapy_logger = logging.getLogger("scapy.runtime")
    old_level = scapy_logger.level
    scapy_logger.setLevel(logging.ERROR)
    arp_request = ARP() / Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request.pdst = arp_request.psrc + "/24"
    sr(arp_request, timeout=1, verbose=False)
    scapy_logger.setLevel(old_level)
    Logger.log("ARP SCAN COMPLETE")


class ARPHandler(AttackHandler):
    arp_table: dict[str, str]
    static_arp_table: dict[str, str]

    def __init__(self):
        """
        Initialize the ARP handler.
        """
        super().__init__(AttackHandler.ARP_HANDLER_ID)
        self.arp_table = {}
        self.static_arp_table = {}

        # run find_device_on_network in a thread

        scanner_thread = threading.Thread(target=find_devices_on_network, daemon=True)
        scanner_thread.start()

    def handle_packet(self, better_packet: MACPacket):
        """
        Handle a network packet.

        :param better_packet: The network packet to handle.
        :type better_packet: MACPacket
        """
        if isinstance(better_packet, ARPPacket):
            self.handle_arp(better_packet)

    def handle_arp(self, arp_packet):
        """
        Handle ARP packets.

        :param arp_packet: The ARP packet to handle.
        :type arp_packet: ARPPacket
        """
        if isinstance(arp_packet, ARPReplyPacket):
            ip = arp_packet.get_source_ip()
            if ip not in self.arp_table:
                self.arp_table[ip] = arp_packet.get_response_mac()
                Logger.log(f"ADD ARP ENTRY: IP {ip} has MAC address {self.arp_table[ip]}")
            elif arp_packet.get_response_mac() != self.arp_table[ip]:
                Logger.log(
                    f"DETECTED ARP POISONING: IP {ip} has multiple MAC addresses: {self.arp_table[ip]} and {arp_packet.get_response_mac()}"
                )

                self.notify(
                    f"IP {ip} has multiple MAC addresses: {self.arp_table[ip]} and {arp_packet.get_response_mac()}"
                )
                self.protect_attack(arp_packet)

    def protect_attack(self, arp_packet):
        """
        Protects against ARP attacks by handling the given packet.

        :param arp_packet: The packet to be handled.
        :type arp_packet: ARPPacket
        """
        try:
            ip = arp_packet.get_source_ip()
            if ip not in self.static_arp_table:
                if ArpUtils.set_static_arp(ip, self.arp_table[ip]):
                    self.static_arp_table[ip] = self.arp_table[ip]
                    self.save_attack(arp_packet, True)
                    Logger.log("ARP PROTECTION SUCCESSFUL")
                    return
                else:
                    Logger.log("ARP PROTECTION FAILED (are you root?)")
                    self.save_attack(arp_packet, False)
                    return
        except Exception as e:
            Logger.log(f"ARP PROTECTION ERROR {e}")
            self.save_attack(arp_packet, False)

    def cleanup(self):
        """
        Cleans up the ARP handler.
        """
        for ip in self.static_arp_table:
            ArpUtils.remove_static_arp(ip)
        Logger.log("ARP CLEANUP SUCCESSFUL")
