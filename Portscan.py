import time

from scapy.layers.inet import TCP, IP

from AttackHandler import AttackHandler
from PacketWrapper import TCPPacket

MAX_SYNS = 100

TIME_TO_CHECK = 1


def is_syn_packet(packet):
    if packet.haslayer(TCP):
        return packet[TCP].flags == 'S'
    return False


class PortscanHandler(AttackHandler):
    ports: list[int]
    time_since_last_check: float
    time_since_last_alert: float
    user_ip: str

    def __init__(self):
        super().__init__(AttackHandler.PORT_HANDLER_ID, AttackHandler.NFQUEUE_HANDLER_TYPE)
        self.ports = []
        self.time_since_last_check = 0
        self.time_since_last_alert = 0

        my_ip_packet = IP()
        self.user_ip = my_ip_packet.src

    def handle_packet(self, better_packet):
        if isinstance(better_packet, TCPPacket):
            if time.time() - self.time_since_last_check > TIME_TO_CHECK:
                self.time_since_last_check = time.time()
                self.ports = []

            self.handle_tcp_packet(better_packet)

    def handle_tcp_packet(self, better_packet):
        if is_syn_packet(better_packet.packet):
            if better_packet.get_source_ip() == self.user_ip:
                return
            if better_packet.get_destination_port() in self.ports:
                return
            self.ports.append(better_packet.get_destination_port())
            counter = len(self.ports)
            if counter > MAX_SYNS:
                if time.time() - self.time_since_last_alert > 60:
                    self.time_since_last_alert = time.time()
                    print("Portscan detected!")
                    self.save_attack(better_packet, False)
                    print(f"Portscan detected from ip {better_packet.get_source_ip()}!")
                    self.notify(f"ip {better_packet.get_source_ip()} is scanning ports!")

    def protect_attack(self, better_packet):
        pass
