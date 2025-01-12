import threading
from ipaddress import IPv4Interface

import requests

import Logger
from AttackHandler import AttackHandler
from PacketWrapper import DNSPacket

RESULT_OK = 200

GOOGLE_DNS = "https://dns.google/resolve"


class DNSHandler(AttackHandler):
    dns_table: dict[str, list[str]]

    def __init__(self):
        """
        Initialize the DNS handler
        """
        super().__init__(AttackHandler.DNS_HANDLER_ID, AttackHandler.NFQUEUE_HANDLER_TYPE)
        self.dns_table = {"dns.google": ["8.8.8.8", "8.8.4.4"]}

    def handle_packet(self, better_packet: DNSPacket):
        """
        Handle a packet
        :param better_packet: the packet to handle
        :return: None
        """
        if isinstance(better_packet, DNSPacket):
            if better_packet.get_type() == DNSPacket.TYPE_QUERY:
                query_thread = threading.Thread(target=self.handle_query, args=(better_packet,), daemon=True)
                query_thread.start()
            elif better_packet.get_type() == DNSPacket.TYPE_ANSWER:
                self.handle_response(better_packet)

    def protect_attack(self, better_packet):
        """
        Protect against an attack
        :param better_packet: the packet to protect against
        :return: None
        """
        try:
            better_packet.drop()
            self.save_attack(better_packet, True)
        except:
            self.save_attack(better_packet, False)

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
        if domain.endswith(".local."):
            return result_ip
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
                    Logger.log("GOOGLE DNS: " + domain + " -> " + result_ips)
            else:
                Logger.log("GOOGLE DNS Error: " + str(res.status_code) + " " + domain)
        except Exception as error:
            Logger.log("GOOGLE DNS Error: " + str(error))
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
        if response in self.dns_table[domain]:
            return
        if not self.is_in_same_subnet(response, self.dns_table[domain]):
            Logger.log(
                f'DNS SPOOFING DETECTED: {domain} has multiple IP addresses: {response} and {self.dns_table[domain]}')
            self.notify(
                f'{domain} has multiple IP addresses: {response} and {self.dns_table[domain]}')
            self.try_protect_attack(better_packet)

    def is_in_same_subnet(self, ip, ip_list):
        """
        Check if an IP address is in the same subnet as any IP address in a list
        :param ip: the IP address to check
        :param ip_list: the list of IP addresses
        :return: True if the IP address is in the same subnet as any IP address in the list, False otherwise
        """
        for ip_in_list in ip_list:
            if IPv4Interface(f'{ip}/24').network == IPv4Interface(f'{ip_in_list}/24').network:
                return True
        return False
