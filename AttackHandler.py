from abc import ABC, abstractmethod


class AttackHandler(ABC):

    DHCP_HANDLER_ID = "DHCP SPOOFING"
    EVIL_TWIN_HANDLER_ID = "Evil Twin"
    ARP_HANDLER_ID = "ARP Poisoning"

    def __init__(self, handler_id):
        self.handler_id = handler_id
        self.enabled = True
    @abstractmethod
    def handle_packet(self, better_packet):
        pass

    @abstractmethod
    def protect_attack(self):
        pass
