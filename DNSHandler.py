from builtins import print

from AttackHandler import AttackHandler
import requests

from PacketWrapper import DNSPacket

RESULT_OK = 200

GOOGLE_DNS = "https://dns.google/resolve"


class DNSHandler(AttackHandler):
    dns_table: dict

    def __init__(self):
        super().__init__(AttackHandler.DNS_HANDLER_ID)
        self.dns_table = {}

    def handle_packet(self, better_packet: DNSPacket):
        if isinstance(better_packet, DNSPacket):
            if better_packet.get_type() == DNSPacket.TYPE_QUERY:
                self.handle_query(better_packet)
            elif better_packet.get_type() == DNSPacket.TYPE_ANSWER:
                self.handle_response(better_packet)

    def protect_attack(self):
        pass

    def handle_query(self, better_packet: DNSPacket):
        if better_packet.get_domain_name() not in self.dns_table:
            domain = better_packet.get_domain_name()
            self.send_query_to_google(domain)

    def send_query_to_google(self, domain):
        result_ip = ""
        res = requests.get(GOOGLE_DNS, params={"name": domain, "type": "A"})
        if res.status_code == RESULT_OK:
            data = res.json()
            if "Answer" in data:
                result_ip = data["Answer"][0]["data"]
                self.dns_table[domain] = result_ip
                print("ADD DNS: " + domain + " -> " + result_ip)
        else:
            print("GOOGLE DNS Error: " + str(res.status_code))
        return result_ip

    def handle_response(self, better_packet):
        domain = better_packet.get_domain_name()
        if better_packet.get_domain_name() not in self.dns_table:
            return
        response = better_packet.get_response()
        if response == "":
            response = self.dns_table[domain]
        if self.dns_table[domain] != response:
            print(
                "DNS Spoofing Detected! " + domain + " -> " + response + " (should be " + self.dns_table[domain] + ")")
