import time

from scapy.layers.inet import TCP

from AttackHandler import AttackHandler
from PacketWrapper import TCPPacket

MAX_SYNS = 100

TIME_TO_CHECK = 1


def is_syn_packet(packet):
    if packet.haslayer(TCP):
        return packet[TCP].flags == 'S'
    return False


class PortscanHandler(AttackHandler):
    counter: int
    time_since_last_check: float
    time_since_last_alert: float

    def __init__(self):
        super().__init__(AttackHandler.PORT_HANDLER_ID)
        self.counter = 0
        self.time_since_last_check = 0
        self.time_since_last_alert = 0

    def handle_packet(self, better_packet):
        if isinstance(better_packet, TCPPacket):
            if time.time() - self.time_since_last_check > TIME_TO_CHECK:
                self.time_since_last_check = time.time()
                self.counter = 0

            self.handle_tcp_packet(better_packet)

    def handle_tcp_packet(self, better_packet):
        if is_syn_packet(better_packet.packet):
            self.counter += 1
            if self.counter > MAX_SYNS:
                if time.time() - self.time_since_last_alert > 60:
                    self.time_since_last_alert = time.time()
                    print("Portscan detected!")
                    self.save_attack(better_packet, False)
                self.counter = 0

    def protect_attack(self):
        pass
