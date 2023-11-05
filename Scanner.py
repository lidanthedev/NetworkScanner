from scapy.sendrecv import sniff


class Scanner:

    def handle_packet(self, packet):
        print(packet.show())

    def scan(self):
        sniff(prn=self.handle_packet)


def main():
    scanner = Scanner()
    scanner.scan()


if __name__ == '__main__':
    main()
