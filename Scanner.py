import PacketWrapper
from scapy.sendrecv import sniff


class Scanner:

    def handle_packet(self, packet):
        better_packet = PacketWrapper.to_better_packet(packet)
        if (better_packet is not None):
            print(better_packet)

    def scan(self):
        sniff(prn=self.handle_packet)


def main():
    scanner = Scanner()
    scanner.scan()


if __name__ == '__main__':
    main()
