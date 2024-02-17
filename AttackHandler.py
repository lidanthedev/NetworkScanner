import time
import uuid
from abc import ABC, abstractmethod

import JsonUtils
import WifiUtils


class AttackHandler(ABC):
    DHCP_HANDLER_ID = "DHCP SPOOFING"
    EVIL_TWIN_HANDLER_ID = "Evil Twin"
    ARP_HANDLER_ID = "ARP Poisoning"
    DNS_HANDLER_ID = "DNS Poisoning"
    PORT_HANDLER_ID = "Port Scan"

    SCAPY_HANDLER_TYPE = "scapy"
    NFQUEUE_HANDLER_TYPE = "nfqueue"

    MODE_OFF = "OFF"
    MODE_DETECT = "DETECT"
    MODE_PROTECT = "PROTECT"

    notifications: list[dict]
    handler_id: str
    handler_type: str
    state: str

    def __init__(self, handler_id, handler_type=SCAPY_HANDLER_TYPE):
        """
        Initialize the attack handler
        :type handler_id: str
        :param handler_id: handler id
        :param handler_type: handler type
        """
        self.notifications = []
        self.handler_id = handler_id
        self.state = self.MODE_PROTECT
        self.handler_type = handler_type

    @abstractmethod
    def handle_packet(self, better_packet):
        """
        Handle a packet
        :param better_packet: the packet to handle
        :return: None
        """
        pass

    def try_protect_attack(self, better_packet):
        """
        Protect against an attack if the mode is set to protect
        :param better_packet: the packet to protect against
        :return: None
        """
        if self.state == self.MODE_PROTECT:
            self.protect_attack(better_packet)
        else:
            self.save_attack(better_packet)

    @abstractmethod
    def protect_attack(self, better_packet):
        """
        Protect against an attack
        :param better_packet: the packet to protect against
        :return: None
        """
        pass

    # NOTE: currently because we have no defenses, this function will be called after detection,
    # when attacks are defended, this function will be called when the attack is detected
    # to fill IS_DEFENDED field
    def save_attack(self, better_packet, is_defended=False):
        """
        Save an attack to the database
        :param better_packet: the packet to save
        :param is_defended: whether the attack was defended or not
        :return: None
        """
        try:
            JsonUtils.save_attack_data({"Attack_name": self.handler_id,
                                        "IP": better_packet.get_source_ip(),
                                        "MAC": better_packet.get_source_mac(),
                                        "WIFI": WifiUtils.get_current_ssid(),
                                        "Time": time.strftime("%H:%M:%S"),
                                        "Date": time.strftime("%d/%m/%Y"),
                                        "Is_Defended": is_defended})
        except Exception as e:
            print("Error saving attack data ", e)

    def notify(self, body, title=None):
        """
        Create a notification
        :param body: notification body
        :param title: notification title
        :return: the notification
        """
        if title is None:
            title = f"{self.handler_id} Detected!"
        notification = {"id": str(uuid.uuid4()), "handler_id": self.handler_id, "title": title, "body": body,
                        "time": int(time.time() * 1000)}
        self.notifications.append(notification)
        return notification

    def cleanup(self):
        """
        Clean up the attack handler
        :return: None
        """
        pass
