from scapy.layers.l2 import Ether
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
        return super().__str__() + f"IP:" \
                            f"  Source IP: {self.get_source_ip()}" \
                            f"  Destination IP: {self.get_destination_ip()}\n" \

    def get_source_ip(self) -> str:
        return self.packet[IP].src

    def get_destination_ip(self) -> str:
        return self.packet[IP].dst


class TCPPacket(IPPacket):

    def __str__(self):
        return super().__str__() + f"TCP:" \
                            f"  Source Port: {self.get_source_port()}" \
                            f"  Destination Port: {self.get_destination_port}" \
                            f"  Protocl: {self.get_protocol()}" \
                            f"  Data: {self.get_data()}\n"

    def get_source_port(self) -> int:
        return self.packet[TCP].sport

    def get_destination_port(self) -> int:
        return self.packet[TCP].dport

    def get_protocol(self) -> str:
        return self.packet[IP].proto

    def get_data(self) -> str:
        return self.packet[TCP].load


def to_better_packet(packet):
    if packet.haslayer(TCP):
        return TCPPacket(packet)
    elif packet.haslayer(IP):
        return IPPacket(packet)
    elif packet.haslayer(Ether):
        return MACPacket(packet)
    else:
        return None
