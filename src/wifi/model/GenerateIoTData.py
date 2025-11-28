import random
import numpy as np
import pandas as pd
categorical_columns = {
    'protocol_type': ['tcp', 'udp']
}
numeric_columns = [
    'duration', 'src_bytes', 'dst_bytes', 
    'num_failed_logins', 'logged_in', 'root_shell', 
    'num_root', 'num_file_creations', 'num_shells',
    'is_host_login', 'is_guest_login', 'count', 'srv_count'
]

def generate_random_ip(node_index):
    return f"192.168.{node_index // 256}.{node_index % 256}"

def generate_random_row(node_ip, all_ips):
    row = []
    protocol_type = random.choice(categorical_columns['protocol_type'])
    row.append(protocol_type)
    if protocol_type == 'tcp':
        service = random.choice(['private', 'http'])
        flag = random.choice(['SF', 'S0'])
    else:
        service = random.choice(['ftp_data', 'other', 'remote_job'])
        flag = 'REJ'

    row.append(service)
    row.append(flag)
    numeric_values = [random.randint(0, 500) for _ in range(len(numeric_columns))]
    row.extend(numeric_values)   
    row.append(node_ip)
    ip_dest = random.choice(all_ips)
    while ip_dest == node_ip:
        ip_dest = random.choice(all_ips)
    row.append(ip_dest)
    loc_x = random.uniform(0, 300)
    loc_y = random.uniform(0, 300)
    row.append(loc_x)
    row.append(loc_y)
    num_root = numeric_values[numeric_columns.index('num_root')]
    if protocol_type == 'tcp':
        attack_class = 'normal' if num_root > 250 else 'attack'
    else:
        attack_class = 'attack' if num_root > 250 else 'normal'
    
    row.append(attack_class)
    return row

def generate_data(num_nodes, total_rows, filename):
    all_ips = [generate_random_ip(i) for i in range(num_nodes)]
    random_data = []
    for node_id, node_ip in enumerate(all_ips, start=1):
        for _ in range(total_rows // num_nodes):
            row = generate_random_row(node_ip, all_ips)
            row.insert(0, node_id) 
            random_data.append(row)
            if len(random_data) == total_rows:
                break
        if len(random_data) == total_rows:
            break

    columns = ['IoT_Node_ID'] + list(categorical_columns.keys()) + ['service', 'flag'] + numeric_columns + ['ip_src', 'ip_dest', 'loc_x', 'loc_y'] + ['attack']
    df = pd.DataFrame(random_data, columns=columns)
    df.to_csv(filename, sep=',', index=False)
    saved_data = pd.read_csv(filename, sep=',')

generate_data(50, 2000, 'Collected_data.txt')

