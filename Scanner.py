import threading
from typing import List

import netfilterqueue
from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP
from scapy.sendrecv import AsyncSniffer

import PacketWrapper
import iptablesUtils
from ARPHandler import ARPHandler
from AttackHandler import AttackHandler
from DHCPHandler import DHCPHandler
from DNSHandler import DNSHandler
from EvilTwinHandler import EvilTwinHandler
from Portscan import PortscanHandler


class Scanner:
    handlers: List[AttackHandler]
    queue: NetfilterQueue
    sniffer: AsyncSniffer
    state: bool

    QUEUE_NUM = 0

    def __init__(self):
        self.handlers = [ARPHandler(), DHCPHandler(), EvilTwinHandler(), DNSHandler(), PortscanHandler()]
        self.queue = NetfilterQueue()
        self.sniffer = AsyncSniffer(prn=self.handle_packet_sniff)
        self.queue_thread = None
        self.state = False

    def handle_packet(self, nfq_packet: netfilterqueue.Packet):
        scapy_packet = IP(nfq_packet.get_payload())

        better_packet = PacketWrapper.to_better_packet(scapy_packet, nfq_packet)
        if better_packet is not None:
            for handler in self.handlers:
                if handler.handler_type == AttackHandler.NFQUEUE_HANDLER_TYPE and handler.enabled:
                    handler.handle_packet(better_packet)
        if not better_packet.dropped:
            nfq_packet.accept()

    def handle_packet_sniff(self, scapy_packet):
        better_packet = PacketWrapper.to_better_packet(scapy_packet, None)
        if better_packet is not None:
            for handler in self.handlers:
                if handler.handler_type == AttackHandler.SCAPY_HANDLER_TYPE and handler.enabled:
                    handler.handle_packet(better_packet)

    def set_attack_state(self, id_attack, state):
        for handler in self.handlers:
            if handler.handler_id == id_attack:
                handler.enabled = state
                return

    def start(self):
        print("Scanner Started")
        self.state = True
        iptablesUtils.add_ip_table(self.QUEUE_NUM)
        self.queue.bind(self.QUEUE_NUM, self.handle_packet)
        self.queue_thread = threading.Thread(target=self.queue.run, daemon=True)
        self.queue_thread.start()
        self.sniffer.start()

    def stop(self):
        print("Scanner Stopped")
        self.state = False
        self.queue.unbind()
        iptablesUtils.remove_ip_table(self.QUEUE_NUM)

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
