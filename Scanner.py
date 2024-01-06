from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, Ether

import PacketWrapper
from AttackHandler import AttackHandler
from DHCPHandler import DHCPHandler
from DNSHandler import DNSHandler
from EvilTwinHandler import EvilTwinHandler
from scapy.sendrecv import sniff
from scapy.sendrecv import AsyncSniffer

from ARPHandler import ARPHandler
from Portscan import PortscanHandler
from netfilterqueue import NetfilterQueue


class Scanner:
    handlers: list[AttackHandler]
    sniffer: AsyncSniffer
    state: bool

    def __init__(self):
        self.handlers = [ARPHandler(), DHCPHandler(), EvilTwinHandler(), DNSHandler(), PortscanHandler()]
        self.queue = netfilterqueue.NetfilterQueue()
        self.state = False

    def handle_packet(self, nfq_packet):
        packet = Ether(nfq_packet.get_payload())
        better_packet = PacketWrapper.to_better_packet(packet, nfq_packet)
        if better_packet is not None:
            for handler in self.handlers:
                if handler.enabled:
                    handler.handle_packet(better_packet)

    def set_attack_state(self, id_attack, state):
        for handler in self.handlers:
            if handler.handler_id == id_attack:
                handler.enabled = state
                return

    def start(self):
        print("Scanner Started")
        self.state = True
        self.queue.bind(0, handle_packet)

    def stop(self):
        print("Scanner Stopped")
        self.state = False
        self.queue.unbind()

    def get_notifications(self):
        notifications = []
        for handler in self.handlers:
            if handler.enabled:
                notifications += handler.notifications
                handler.notifications = []
        return notifications


def main():
    scanner = Scanner()
    scanner.start()


    while True:
        pass


if __name__ == "__main__":
    main()
