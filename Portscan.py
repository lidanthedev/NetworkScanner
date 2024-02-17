import time

from scapy.layers.inet import TCP, IP

from AttackHandler import AttackHandler
from PacketWrapper import TCPPacket

MAX_SYNS = 100

TIME_TO_CHECK = 1


def is_syn_packet(packet):
    """
    Check if the packet is a syn packet
    :param packet: the packet to check
    :return: true if the packet is a syn packet, false otherwise
    """
    if packet.haslayer(TCP):
        return packet[TCP].flags == 'S'
    return False


class PortscanHandler(AttackHandler):
    ip_ports_map: dict[str, list[int]]
    blacklisted_ips: list[str]
    time_since_last_check: float
    time_since_last_alert: float
    time_since_last_save: float
    user_ip: str

    def __init__(self):
        """
        Initialize the portscan handler
        """
        super().__init__(AttackHandler.PORT_HANDLER_ID, AttackHandler.NFQUEUE_HANDLER_TYPE)
        self.ip_ports_map = {}
        self.blacklisted_ips = []
        self.time_since_last_check = 0
        self.time_since_last_alert = 0
        self.time_since_last_save = 0

        my_ip_packet = IP()
        self.user_ip = my_ip_packet.src

    def handle_packet(self, better_packet):
        """
        Handle a packet
        :param better_packet: the packet to handle
        :return: None
        """
        if isinstance(better_packet, TCPPacket):
            if time.time() - self.time_since_last_check > TIME_TO_CHECK:
                self.time_since_last_check = time.time()
                self.ip_ports_map = {}

            self.handle_tcp_packet(better_packet)

    def handle_tcp_packet(self, better_packet):
        """
        Handle a tcp packet
        :param better_packet: the packet to handle
        :return: None
        """
        if is_syn_packet(better_packet.packet):
            if better_packet.get_source_ip() == self.user_ip:
                return
            if better_packet.get_destination_port() in self.ip_ports_map:
                return
            if better_packet.get_source_ip() not in self.ip_ports_map:
                self.ip_ports_map[better_packet.get_source_ip()] = []
            self.ip_ports_map[better_packet.get_source_ip()].append(better_packet.get_destination_port())
            counter = len(self.ip_ports_map[better_packet.get_source_ip()])
            if better_packet.get_source_ip() in self.blacklisted_ips:
                self.try_protect_attack(better_packet)
            elif counter > MAX_SYNS:
                self.try_protect_attack(better_packet)
                if time.time() - self.time_since_last_alert > 60:
                    self.time_since_last_alert = time.time()
                    print("Portscan detected!")
                    print(f"Portscan detected from ip {better_packet.get_source_ip()}!")
                    self.notify(f"ip {better_packet.get_source_ip()} is scanning ports!")

    def protect_attack(self, better_packet):
        """
        Protect from an attack
        :param better_packet: the packet to protect from
        :return: None
        """
        try:
            if better_packet.get_source_ip() not in self.blacklisted_ips:
                self.blacklisted_ips.append(better_packet.get_source_ip())
                print(f"Blacklisted ip {better_packet.get_source_ip()}")
            better_packet.drop()
            if time.time() - self.time_since_last_save > 60:
                self.time_since_last_save = time.time()
                self.save_attack(better_packet, True)
        except IndexError:
            if time.time() - self.time_since_last_save > 60:
                self.time_since_last_save = time.time()
                self.save_attack(better_packet, False)

