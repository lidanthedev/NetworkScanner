from builtins import print

from AttackHandler import AttackHandler
import requests

from PacketWrapper import DNSPacket

RESULT_OK = 200

GOOGLE_DNS = "https://dns.google/resolve"


class DNSHandler(AttackHandler):
    dns_table: dict[str, list[str]]

    def __init__(self):
        """
        Initialize the DNS handler
        """
        super().__init__(AttackHandler.DNS_HANDLER_ID)
        self.dns_table = {}

    def handle_packet(self, better_packet: DNSPacket):
        """
        Handle a packet
        :param better_packet: the packet to handle
        :return: None
        """
        if isinstance(better_packet, DNSPacket):
            if better_packet.get_type() == DNSPacket.TYPE_QUERY:
                self.handle_query(better_packet)
            elif better_packet.get_type() == DNSPacket.TYPE_ANSWER:
                self.handle_response(better_packet)

    def protect_attack(self, better_packet):
        """
        Protect against an attack
        :param better_packet: the packet to protect against
        :return: None
        """
        pass

    def handle_query(self, better_packet: DNSPacket):
        """
        Handle a DNS query
        :param better_packet: the packet to handle
        :return: None
        """
        if better_packet.get_domain_name() not in self.dns_table:
            domain = better_packet.get_domain_name()
            self.send_query_to_google(domain)

    def send_query_to_google(self, domain):
        """
        Send a DNS query to Google's DNS server
        :param domain: the domain to query
        :return: None
        """
        result_ip = ""
        try:
            res = requests.get(GOOGLE_DNS, params={"name": domain, "type": "A"})
            if res.status_code == RESULT_OK:
                data = res.json()
                addresses = []
                if "Answer" in data:
                    for answer in data["Answer"]:
                        if answer["type"] == DNSPacket.A_RECORD:
                            addresses.append(answer["data"])
                if len(addresses) > 0:
                    result_ips = ", ".join(addresses)
                    self.dns_table[domain] = addresses
                    print("GOOGLE DNS: " + domain + " -> " + result_ips)
            else:
                print("GOOGLE DNS Error: " + str(res.status_code))
        except Exception as error:
            print("GOOGLE DNS Error: " + str(error))
        return result_ip

    def handle_response(self, better_packet):
        """
        Handle a DNS response
        :param better_packet: the packet to handle
        :return: None
        """
        domain = better_packet.get_domain_name()
        if domain not in self.dns_table:
            return
        response = better_packet.get_response()
        if response == "":
            response = self.dns_table[domain][0]
        if response not in self.dns_table[domain]:
            print(
                f'DNS SPOOFING DETECTED: {domain} has multiple IP addresses: {response} and {self.dns_table[domain]}')
            self.save_attack(better_packet, False)
            self.notify(
                f'{domain} has multiple IP addresses: {response} and {self.dns_table[domain]}')