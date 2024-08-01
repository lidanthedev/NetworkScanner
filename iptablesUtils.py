import subprocess
import Logger

import iptc


def add_ip_table(id_table):
    """
    Add a new IP table to the INPUT chain.
    :param id_table: The ID of the table.
    :return None
    """
    rule = make_rule(id_table)

    # Get the "INPUT" chain
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

    # Insert the rule into the chain
    chain.insert_rule(rule)


def remove_ip_table(id_table):
    """
    Remove an IP table from the INPUT chain.
    :param id_table: The ID of the table.
    :return: None
    """
    # Create a new rule
    rule = make_rule(id_table)

    # Get the "INPUT" chain
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

    # Delete the rule from the chain
    chain.delete_rule(rule)


# manual disable: sudo iptables -D INPUT -j NFQUEUE --queue-num 0

def make_rule(id_table):
    """
    Make a rule for the INPUT chain.
    :param id_table: The ID of the table.
    :return: The rule.
    """
    rule = iptc.Rule()
    rule.src = "!127.0.0.1"
    # Create a target for the rule
    target = iptc.Target(rule, "NFQUEUE")
    # Set the queue number to the target
    target.set_parameter("queue-num", str(id_table))
    # Set the rule's target
    rule.target = target
    return rule


# manual disable: sudo iptables -L INPUT --line-numbers
# sudo iptables -D INPUT [NUM]


def block_mac_address(mac_to_block: str):
    """
    Will block all packets from given mac address
    :param mac_to_block: The mac to block
    :return: None
    """
    try:
        command = f"iptables -A INPUT -m mac --mac-source {mac_to_block} -j DROP"
        subprocess.run(command, shell=True)
    except subprocess.CalledProcessError as e:
        Logger.log(f"Something went wrong while blocking a mac address, error is: {e}")


def unblock_mac_address(mac_to_unblock: str):
    """
    Will unblock all the given mac adress
    :param mac_to_unblock: the mac to unblock
    :return: None
    """
    try:
        mac_to_unblock = mac_to_unblock.upper()
        # Get the line number of the rule to be removed
        command = f"iptables -L INPUT -n -v --line-numbers | grep ד{mac_to_unblock}"
        result = subprocess.check_output(command, shell=True)
        lines = result.decode().split('\n')
        for line in lines:
            if mac_to_unblock in line:
                # Extract the line number
                line_num = line.split(' ')[0]
                # Remove the rule
                command = f"iptables -D INPUT {line_num}"

                subprocess.run(command, shell=True)
    except subprocess.CalledProcessError as e:
        Logger.log(f"Something went wrong while unblocking a mac address, error is: {e}")

