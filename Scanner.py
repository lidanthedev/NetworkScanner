import PacketWrapper
from AttackHandler import AttackHandler
from DHCPHandler import DHCPHandler
from scapy.sendrecv import sniff
from scapy.sendrecv import AsyncSniffer

from ARPHandler import ARPHandler


class Scanner:
    handlers: list[AttackHandler]
    sniffer: AsyncSniffer
    state: bool

    def __init__(self):
        self.handlers = [ARPHandler(), DHCPHandler()]
        self.sniffer = AsyncSniffer(prn=self.handle_packet)
        self.state = False

    def handle_packet(self, packet):
        better_packet = PacketWrapper.to_better_packet(packet)
        if better_packet is not None:
            for handler in self.handlers:
                handler.handle_packet(better_packet)

    def start(self):
        print("Scanner Started")
        self.state = True
        self.sniffer.start()

    def stop(self):
        print("Scanner Stopped")
        self.state = False
        self.sniffer.stop()


def main():
    scanner = Scanner()
    scanner.start()

    while True:
        pass


if __name__ == "__main__":
    main()
