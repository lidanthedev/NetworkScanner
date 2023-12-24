import random
import time
import uuid
from abc import ABC, abstractmethod
import JsonUtils
import WifiUtils
import time

class AttackHandler(ABC):
    DHCP_HANDLER_ID = "DHCP SPOOFING"
    EVIL_TWIN_HANDLER_ID = "Evil Twin"
    ARP_HANDLER_ID = "ARP Poisoning"
    DNS_HANDLER_ID = "DNS Poisoning"
    PORT_HANDLER_ID = "Port Scan"

    notifications: list[dict]

    def __init__(self, handler_id):
        self.notifications = []
        self.handler_id = handler_id
        self.enabled = True

    @abstractmethod
    def handle_packet(self, better_packet):
        pass

    @abstractmethod
    def protect_attack(self):
        pass

    # NOTE: currently because we have no defenses, this function will be called after detection,
    # when attacks are defended, this function will be called when the attack is detected
    # to fill IS_DEFENDED field
    def save_attack(self, better_packet, is_defended):
        JsonUtils.save_attack_data({"Attack_name": self.handler_id,
                                    "IP": better_packet.get_source_ip(),
                                    "MAC": better_packet.get_source_mac(),
                                    "WIFI": WifiUtils.get_current_ssid(),
                                    "Time": time.strftime("%H:%M:%S"),
                                    "Date": time.strftime("%d/%m/%Y"),
                                    "Is_Defended": is_defended})

    def notify(self, body, title=None):
        if title is None:
            title = f"{self.handler_id} Detected!"
        notification = {"id": str(uuid.uuid4()), "handler_id": self.handler_id, "title": title, "body": body,
                        "time": int(time.time() * 1000)}
        self.notifications.append(notification)
        return notification
