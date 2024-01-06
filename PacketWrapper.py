from scapy.layers.dns import DNS
from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, TCP
from scapy.packet import Packet
from scapy.layers.dhcp import DHCP
import dataclasses
import netfilterqueue

ARP_REPLY_CODE = 2

ARP_REQUEST_CODE = 1


@dataclasses.dataclass
class MACPacket:
    scapy_packet: Packet
    nfq_packet: netfilterqueue.packet

    def __init__(self, scapy_packet: Packet, nfq_packet: netfilterqueue.packet):
        self.scapy_packet = scapy_packet
        self.nfq_packet = nfq_packet

    def __str__(self):
        return f"MAC:" \
               f"  Source MAC: {self.get_source_mac()}" \
               f"  Destination MAC: {self.get_destination_mac()}\n"

    def get_scapy_packet(self) -> Packet:
        return self.scapy_packet

    def get_nfq_packet(self) -> netfilterqueue.packet:
        return self.nfq_packet

    def get_source_mac(self) -> str:
        return self.scapy_packet[Ether].src

    def get_destination_mac(self) -> str:
        return self.scapy_packet[Ether].dst


class IPPacket(MACPacket):

    def __str__(self):
        return super().__str__() + f"IP: " \
                                   f"  Source IP: {self.get_source_ip()}" \
                                   f"  Destination IP: {self.get_destination_ip()}\n"

    def get_source_ip(self) -> str:
        return self.scapy_packet[IP].src

    def get_destination_ip(self) -> str:
        return self.scapy_packet[IP].dst


class TCPPacket(IPPacket):

    def __str__(self):
        return super().__str__() + f"TCP:" \
                                   f"  Source Port: {self.get_source_port()}" \
                                   f"  Destination Port: {self.get_destination_port()}\n"

    def get_source_port(self) -> int:
        return self.scapy_packet[TCP].sport

    def get_destination_port(self) -> int:
        return self.scapy_packet[TCP].dport


class DHCPPacket(IPPacket):
    DISCOVER = 1
    OFFER = 2
    REQUEST = 3
    DECLINE = 4
    ACK = 5

    def __str__(self):
        return super().__str__() + f"DHCP:" \
                                   f"  DHCP Type: {self.get_dhcp_type()}\n"

    def get_dhcp_type(self) -> int:
        return self.scapy_packet[DHCP].options[0][1]


class ARPPacket(MACPacket):
    def __str__(self):
        return super().__str__() + f"ARP Request:" \
                                   f"  Source IP: {self.get_source_ip()}" \
                                   f"  Destination IP: {self.get_destination_ip()}\n"

    def get_source_ip(self) -> str:
        return self.scapy_packet[ARP].psrc

    def get_destination_ip(self) -> str:
        return self.scapy_packet[ARP].pdst


class ARPReplyPacket(ARPPacket):
    def __str__(self):
        return super().__str__() + f"ARP Reply:" \
                                   f"  Source IP: {self.get_source_ip()}" \
                                   f"  Destination IP: {self.get_destination_ip()}" \
                                   f"  Reply MAC: {self.get_response_mac()}\n"

    def get_response_mac(self) -> str:
        return self.scapy_packet[ARP].hwsrc


class DNSPacket(MACPacket):
    TYPE_QUERY = "Query"
    TYPE_ANSWER = "Answer"
    TYPE_OTHER = "Other"

    A_RECORD = 1

    def __str__(self):
        return super().__str__() + f"DNS:" \
                                   f"  Domain Name: {self.get_domain_name()}\n"

    def get_domain_name(self) -> str:
        try:
            if self.scapy_packet[DNS].qd is not None:
                return self.scapy_packet[DNS].qd.qname.decode("utf-8")
            elif self.scapy_packet[DNS].an is not None:
                return self.scapy_packet[DNS].an.rdata
        finally:
            return ""

    def get_type(self) -> str:
        if self.scapy_packet[DNS].an is not None:
            return self.TYPE_ANSWER
        elif self.scapy_packet[DNS].qd is not None:
            return self.TYPE_QUERY

        return self.TYPE_OTHER

    def get_response(self) -> str:
        if self.scapy_packet[DNS].an is not None:
            for answer in self.scapy_packet[DNS].an:
                if answer.type == self.A_RECORD:
                    return answer.rdata

        return ""


def to_better_packet(scapy_packet, nfq_packet):
    if scapy_packet.haslayer(DHCP) and scapy_packet.haslayer(Ether) and scapy_packet.haslayer(IP):
        return DHCPPacket(scapy_packet, nfq_packet)
    if scapy_packet.haslayer(TCP) and scapy_packet.haslayer(IP) and scapy_packet.haslayer(Ether):
        return TCPPacket(scapy_packet, nfq_packet)
    elif scapy_packet.haslayer(IP) and scapy_packet.haslayer(Ether):
        return IPPacket(scapy_packet, nfq_packet)
    elif scapy_packet.haslayer(DNS) and scapy_packet.haslayer(Ether):
        return DNSPacket(scapy_packet, nfq_packet)
    elif scapy_packet.haslayer(ARP) and scapy_packet.haslayer(Ether):
        if scapy_packet[ARP].op == ARP_REQUEST_CODE:
            return ARPPacket(scapy_packet, nfq_packet)
        elif scapy_packet[ARP].op == ARP_REPLY_CODE:
            return ARPReplyPacket(scapy_packet, nfq_packet)
    elif scapy_packet.haslayer(Ether):
        return MACPacket(scapy_packet, nfq_packet)
    else:
        return None
    return None
