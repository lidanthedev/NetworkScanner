from abc import ABC, abstractmethod


class AttackHandler(ABC):
    @abstractmethod
    def handle_packet(self, better_packet):
        pass

    @abstractmethod
    def protect_attack(self):
        pass
