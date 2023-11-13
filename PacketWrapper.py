from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, TCP
from scapy.packet import Packet
import dataclasses


@dataclasses.dataclass
class MACPacket:
    packet: Packet

    def __init__(self, packet: Packet):
        self.packet = packet

    def __str__(self):
        return f"MAC:" \
               f"  Source MAC: {self.get_source_mac()}" \
               f"  Destination MAC: {self.get_destination_mac()}\n"

    def get_packet(self) -> Packet:
        return self.packet

    def get_source_mac(self) -> str:
        return self.packet[Ether].src

    def get_destination_mac(self) -> str:
        return self.packet[Ether].dst


class IPPacket(MACPacket):

    def __str__(self):
        return super().__str__() + f"IP: " \
                                   f"  Source IP: {self.get_source_ip()}" \
                                   f"  Destination IP: {self.get_destination_ip()}\n"

    def get_source_ip(self) -> str:
        return self.packet[IP].src

    def get_destination_ip(self) -> str:
        return self.packet[IP].dst


class TCPPacket(IPPacket):

    def __str__(self):
        return super().__str__() + f"TCP:" \
                                   f"  Source Port: {self.get_source_port()}" \
                                   f"  Destination Port: {self.get_destination_port()}\n"

    def get_source_port(self) -> int:
        return self.packet[TCP].sport

    def get_destination_port(self) -> int:
        return self.packet[TCP].dport


class ARPPacket(MACPacket):
    def __str__(self):
        return super().__str__() + f"ARP Request:" \
                                   f"  Source IP: {self.get_source_ip()}" \
                                   f"  Destination IP: {self.get_destination_ip()}\n"

    def get_source_ip(self) -> str:
        return self.packet[ARP].psrc

    def get_destination_ip(self) -> str:
        return self.packet[ARP].pdst


class ARPReplyPacket(ARPPacket):
    def __str__(self):
        return super().__str__() + f"ARP Reply:" \
                                   f"  Source IP: {self.get_source_ip()}" \
                                   f"  Destination IP: {self.get_destination_ip()}\n"

    def get_response_mac(self) -> str:
        return self.packet[ARP].hwsrc


def to_better_packet(packet):
    if packet.haslayer(TCP) and packet.haslayer(IP) and packet.haslayer(Ether):
        return TCPPacket(packet)
    elif packet.haslayer(IP) and packet.haslayer(Ether):
        return IPPacket(packet)
    elif packet.haslayer(ARP) and packet.haslayer(Ether):
        if packet[ARP].op == 1:  # ARP Request
            return ARPPacket(packet)
        elif packet[ARP].op == 2:  # ARP Reply
            return ARPReplyPacket(packet)
    elif packet.haslayer(Ether):
        return MACPacket(packet)
    else:
        return None
    return None
