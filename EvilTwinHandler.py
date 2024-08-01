import collections
import subprocess
import time

from AttackHandler import AttackHandler
import Logger
import WifiUtils


class EvilTwinHandler(AttackHandler):
    TIME_TO_CHECK_EVILTWIN = 20
    MIN_FREQUENCY = 2
    MAX_FREQUENCY = 3

    def __init__(self):
        """
        Initialize the Evil Twin handler
        """
        super().__init__(AttackHandler.EVIL_TWIN_HANDLER_ID)
        self.time_since_last_check = time.perf_counter()

    def handle_packet(self, better_packet):
        """
        Handle a packet
        :param better_packet: the packet to handle
        :return: None
        """
        # we don't want to check for each packet, that would be a waste
        if time.perf_counter() - self.time_since_last_check > self.TIME_TO_CHECK_EVILTWIN:
            self.time_since_last_check = time.perf_counter()

            current_networks = WifiUtils.get_wifi_networks(EvilTwinHandler.MIN_FREQUENCY, EvilTwinHandler.MAX_FREQUENCY)
            # get all networks that appear with the same name more than once
            duplicates = [item for item, count in collections.Counter(current_networks).items() if count > 1]
            if "" in duplicates:
                duplicates.remove("")

            if len(duplicates) > 0:
                Logger.log(f"Evil Twin Detected, networks that appear more than once: {duplicates}")
                self.notify(f"networks that appear more than once: {duplicates}")

    def protect_attack(self, better_packet):
        """
        Protect against an attack
        :param better_packet: the packet to protect against
        :return: None
        """
        pass
