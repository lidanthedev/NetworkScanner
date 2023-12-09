from abc import ABC, abstractmethod


class AttackHandler(ABC):

    DHCP_HANDLER_ID = 1
    EVIL_TWIN_HANDLER_ID = 2
    ARP_HANDLER_ID = 3

    def __init__(self, handler_id):
        self.handler_id = handler_id
    @abstractmethod
    def handle_packet(self, better_packet):
        pass

    @abstractmethod
    def protect_attack(self):
        pass
