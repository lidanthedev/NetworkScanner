import subprocess


def set_static_arp(ip, mac):
    """
    Set a static ARP entry.
    :param ip: the IP address
    :param mac: the MAC address
    :return: None
    """
    process = subprocess.run(["arp", "-s", ip, mac], capture_output=True, text=True)
    return process.returncode == 0



def remove_static_arp(ip):
    """
    Remove a static ARP entry.
    :param ip: the IP address
    :return: None
    """
    process = subprocess.run(["arp", "-d", ip], capture_output=True, text=True)
    return process.returncode == 0
