import subprocess

def add_ip_table(id_table):
    iptables_cmd = f"sudo iptables -A INPUT -j NFQUEUE --queue-num {id_table}"
    print(f"Initiating an IP table with id - {id_table}")
    subprocess.run(iptables_cmd, shell=True, check=True)

def remove_ip_table(id_table):
    iptables_cmd = f"sudo iptables -D INPUT -j NFQUEUE --queue-num {id_table}"
    print(f"Removing an IP table with id - {id_table}")
    subprocess.run(iptables_cmd, shell=True, check=True)