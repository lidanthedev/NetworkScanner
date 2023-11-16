import PacketWrapper
from AttackHandler import AttackHandler
from DHCPHandler import DHCPHandler
from scapy.sendrecv import sniff


class Scanner:
    attackHandlers: list[AttackHandler]
    def __init__(self):
        self.attackHandlers = [DHCPHandler()]

    def handle_packet(self, packet):
        better_packet = PacketWrapper.to_better_packet(packet)
        if (better_packet is not None):
            for attackHandler in self.attackHandlers:
                attackHandler.handle_packet(better_packet)

    def scan(self):
        sniff(prn=self.handle_packet)


def main():
    scanner = Scanner()
    scanner.scan()


if __name__ == '__main__':
    main()
