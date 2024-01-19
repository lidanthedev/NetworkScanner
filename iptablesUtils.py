import iptc


def add_ip_table(id_table):
    # Create a new rule
    rule = iptc.Rule()

    # Create a target for the rule
    target = iptc.Target(rule, "NFQUEUE")

    # Set the queue number to the target
    target.set_parameter("queue-num", str(id_table))

    # Set the rule's target
    rule.target = target

    # Get the "INPUT" chain
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

    # Insert the rule into the chain
    chain.insert_rule(rule)


def remove_ip_table(id_table):
    # Create a new rule
    rule = iptc.Rule()

    # Create a target for the rule
    target = iptc.Target(rule, "NFQUEUE")

    # Set the queue number to the target
    target.set_parameter("queue-num", str(id_table))

    # Set the rule's target
    rule.target = target

    # Get the "INPUT" chain
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

    # Delete the rule from the chain
    chain.delete_rule(rule)

# manual disable: sudo iptables -D INPUT -j NFQUEUE --queue-num 0