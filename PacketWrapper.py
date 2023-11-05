from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from scapy.packet import Packet
import dataclasses


@dataclasses.dataclass
class MACPacket:
    packet: Packet

    def __init__(self, packet: Packet):
        self.packet = packet

    def get_packet(self) -> Packet:
        return self.packet

    def get_source_mac(self) -> str:
        return self.packet[Ether].src

    def get_destination_mac(self) -> str:
        return self.packet[Ether].dst


class IPPacket(MACPacket):
    def get_source_ip(self) -> str:
        return self.packet[IP].src

    def get_destination_ip(self) -> str:
        return self.packet[IP].dst


class TCPPacket(IPPacket):
    def get_source_port(self) -> int:
        return self.packet[TCP].sport

    def get_destination_port(self) -> int:
        return self.packet[TCP].dport

    def get_protocol(self) -> str:
        return self.packet[IP].proto

    def get_data(self) -> str:
        return self.packet[TCP].load
