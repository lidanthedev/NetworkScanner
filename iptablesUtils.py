import iptc


def add_ip_table(id_table):
    """
    Add a new IP table to the INPUT chain.
    :param id_table: The ID of the table.
    :return None
    """
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
    """
    Remove an IP table from the INPUT chain.
    :param id_table: The ID of the table.
    :return: None
    """
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


def add_mac_block_ip_table(mac_address: str):
    # Create an IPTables object
    iptables = iptc.IPTables()

    # Create a rule to block traffic from the specified MAC address
    rule = iptc.Rule()
    rule.add_match(iptc.Match('mac', '--mac-source', mac_address))
    rule.target = iptc.Target('DROP')

    # Apply the rule to the INPUT chain on all interfaces
    iptables.table['filter'].chain['INPUT'].append_rule(rule, interface=None)

    # Save the rules
    iptables.save()

    print(f"Successfully added an ip-table to block {mac_address} and traffic from it")


def remove_mac_block_ip_table(mac_address: str):
    # Create an IPTables object
    iptables = iptc.IPTables()

    # Find the rule that blocks traffic from the specified MAC address
    existing_rules = iptables.table['filter'].chain['INPUT'].rules
    rule_to_remove = None

    for rule in existing_rules:
        if (
                rule.matches
                and rule.matches[0].name == 'mac'
                and rule.matches[0].args[0] == '--mac-source'
                and rule.matches[0].args[1] == mac_address
        ):
            rule_to_remove = rule
            break

    # Remove the rule from the INPUT chain
    if rule_to_remove:
        iptables.table['filter'].chain['INPUT'].remove_rule(rule_to_remove)

        # Save the updated rules
        iptables.save()

        print(f"Removed block for traffic from MAC address {mac_address}")
    else:
        print(f"No existing rule found for MAC address {mac_address}")