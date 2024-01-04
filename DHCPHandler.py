import time

from AttackHandler import AttackHandler
from scapy.layers.dhcp import DHCP

import JsonUtils
import WifiUtils

class DHCPHandler(AttackHandler):

    def __init__(self):
        super().__init__(AttackHandler.DHCP_HANDLER_ID)
        self.mac_table = {}

    def handle_packet(self, better_packet):
        if DHCP not in better_packet.packet:
            return

        # if joined a new network
        if self.is_packet_dhcp_ack(better_packet):
            # we sleep here to make sure the device successfully gets
            # connected to the network before trying to pull
            # the ssid since the function requires you being in it
            time.sleep(2)
            network_name = WifiUtils.get_current_ssid()

            if network_name in self.mac_table:
                # if we already connected to this net work before and the mac of the
                # device that gave us the ack command the first time we joined it
                # is not the same then there is an attack going on
                if self.mac_table[network_name] != better_packet.get_source_mac():
                    print("DHCP ATTACK DETECTED!!!!!!")
                    self.save_attack(better_packet, False)
                    self.notify(f"MAC doesn't match {self.mac_table[network_name]} with {better_packet.get_source_mac()}")
            # save the mac address of the joined network if it's the first time joining it
            else:
                print(f"ADD DHCP: {network_name} {better_packet.get_source_mac()}")
                self.mac_table[network_name] = better_packet.get_source_mac()

    def protect_attack(self):
        pass

    def is_packet_dhcp_ack(self, better_packet):
        return better_packet.packet[DHCP].options[0][1] == 5

