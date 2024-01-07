import multiprocessing
import threading

import scapy.layers.http

from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, Ether
from scapy.layers.http import HTTP
from typing import List

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
import iptablesUtils


class Scanner:
    handlers: List[AttackHandler]
    queue: NetfilterQueue
    state: bool

    QUEUE_NUM = 0

    def __init__(self):
        self.handlers = [ARPHandler(), DHCPHandler(), EvilTwinHandler(), DNSHandler(), PortscanHandler()]
        self.queue = NetfilterQueue()
        self.queue_proc = None
        self.state = False

    def handle_packet(self, nfq_packet):
        scapy_packet = Ether(nfq_packet.get_payload())

        better_packet = PacketWrapper.to_better_packet(scapy_packet, nfq_packet)
        if better_packet is not None:
            for handler in self.handlers:
                if handler.enabled:
                    handler.handle_packet(better_packet)

        nfq_packet.accept()

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
        self.queue_proc = multiprocessing.Process(target=self.queue.run)
        self.queue_proc.start()

    def stop(self):
        print("Scanner Stopped")
        self.state = False
        self.queue.unbind()
        self.queue_proc.terminate()
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
