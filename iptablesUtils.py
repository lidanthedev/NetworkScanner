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