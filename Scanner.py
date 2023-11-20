import PacketWrapper
from AttackHandler import AttackHandler
from DHCPHandler import DHCPHandler
from scapy.sendrecv import sniff
from scapy.sendrecv import AsyncSniffer

from ARPHandler import ARPHandler


class Scanner:
    handlers: list[AttackHandler]

    def __init__(self):
        self.handlers = [ARPHandler(), DHCPHandler()]

    def handle_packet(self, packet):
        better_packet = PacketWrapper.to_better_packet(packet)
        if better_packet is not None:
            for handler in self.handlers:
                handler.handle_packet(better_packet)

    def scan(self):
        sniff(prn=self.handle_packet)


def main():
    scanner = Scanner()
    scanner.scan()


if __name__ == '__main__':
    main()
