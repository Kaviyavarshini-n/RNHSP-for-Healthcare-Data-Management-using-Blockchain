import csv
import json
import random
import time
from getpass import getpass
import requests
from threading import Thread, Lock

# Load user data from CSV file
def load_user_data(file_path):
    with open(file_path, newline='') as csvfile:
        data = list(csv.DictReader(csvfile))
    return data

class AccessControl:
    def __init__(self):
        self.user_roles = {
            "admin": ["read", "write", "revoke"],
            "doctor": ["read", "write"],
            "patient": ["read"]
        }

    def check_permission(self, role, action):
        return action in self.user_roles.get(role.lower(), [])

# Paxos Node Class
class PaxosNode:
    def __init__(self, node_id, quorum_size):
        self.node_id = node_id
        self.quorum_size = quorum_size
        self.proposal_number = 0
        self.lock = Lock()
        self.promises = {}
        self.accepted_values = {}

    def propose(self, value):
        with self.lock:
            self.proposal_number += 1
            proposal_id = (self.proposal_number, self.node_id)

        promises_received = 0
        for node in PaxosCluster.nodes:
            if node.promise(proposal_id):
                promises_received += 1

        if promises_received >= self.quorum_size:
            for node in PaxosCluster.nodes:
                if not node.accept(proposal_id, value):
                    return False
            return True
        return False

    def promise(self, proposal_id):
        with self.lock:
            if proposal_id > self.promises.get(self.node_id, (0, -1)):
                self.promises[self.node_id] = proposal_id
                return True
        return False

    def accept(self, proposal_id, value):
        with self.lock:
            if proposal_id >= self.promises.get(self.node_id, (0, -1)):
                self.accepted_values[self.node_id] = value
                return True
        return False

class PaxosCluster:
    nodes = []

    @classmethod
    def initialize(cls, num_nodes, quorum_size):
        cls.nodes = [PaxosNode(i, quorum_size) for i in range(num_nodes)]

# Initialize Paxos Cluster
NUM_NODES = 5
QUORUM_SIZE = 3
PaxosCluster.initialize(NUM_NODES, QUORUM_SIZE)

# Generate random passwords for roles
def generate_random_password():
    return f"{random.randint(100000, 999999)}"

def print_password_conditions(role, password=None, user_passwords=None):
    if role == "admin":
        print(f"Admin Password: {password}")
    elif role == "doctor":
        print(f"Doctor Password: {password}")
    elif role == "patient":
        print("Patient User IDs and Passwords:")
        for user_id, user_password in user_passwords.items():
            print(f"User ID: {user_id}, Password: {user_password}")

def password_is_valid(role, password, generated_password, user_passwords=None):
    if role in ["admin", "doctor"]:
        return password == generated_password
    elif role == "patient":
        return password in user_passwords.values()
    else:
        return False

def get_role_and_password():
    valid_roles = ["admin", "doctor", "patient"]
    while True:
        user_role = input("Enter your role (admin/doctor/patient): ").lower()
        if user_role not in valid_roles:
            print("Wrong choice. Please enter a valid role (admin/doctor/patient).")
            continue

        if user_role in ["admin", "doctor"]:
            generated_password = generate_random_password()
            print_password_conditions(user_role, password=generated_password)
            user_passwords = None
        elif user_role == "patient":
            user_passwords = {f"User{i+1}": generate_random_password() for i in range(100)}
            print_password_conditions(user_role, user_passwords=user_passwords)
            generated_password = None

        while True:
            password = getpass("Enter password: ")
            if password_is_valid(user_role, password, generated_password, user_passwords if user_role == "patient" else None):
                print("Password is valid.")
                return user_role, password, generated_password, user_passwords
            else:
                print(f"Password is invalid for {user_role}. Please try again.")

def upload_to_ipfs(data):
    try:
        ipfs_url = 'http://127.0.0.1:5001/api/v0/add'
        files = {'file': ('data.json', data)}
        response = requests.post(ipfs_url, files=files)
        res_json = response.json()
        ipfs_hash = res_json['Hash']
        ipfs_gateway_url = f"https://ipfs.io/ipfs/{ipfs_hash}"
        print(f"Uploaded data to IPFS. Public download link: {ipfs_gateway_url}")
        return ipfs_hash
    except Exception as e:
        print(f"Error uploading to IPFS: {e}")
        return None

def perform_paxos_consensus(action):
    proposer = random.choice(PaxosCluster.nodes)
    if proposer.propose(action):
        print(f"Consensus reached: Action '{action}' approved.")
        return True
    else:
        print(f"Consensus failed: Action '{action}' not approved.")
        return False

if __name__ == "__main__":
    user_data_file = 'user_health_data.csv'
    data = load_user_data(user_data_file)
    user_role, password, generated_password, user_passwords = get_role_and_password()
    ac = AccessControl()

    if not ac.check_permission(user_role, "read"):
        print("Access Denied!")
    else:
        if perform_paxos_consensus("grant_access"):
            print("Access Granted!")
            time.sleep(3)

            if user_role == "admin":
                ipfs_hash = upload_to_ipfs(json.dumps(data))
                print(f"All data uploaded to IPFS at hash: {ipfs_hash}")

            elif user_role == "doctor":
                doctor_records = [
                    {
                        "User ID": record['Name'],
                        "Medical Condition": record['Medical Condition'],
                        "Test Results": record['Test Results']
                    }
                    for record in data
                ]
                ipfs_hash = upload_to_ipfs(json.dumps(doctor_records))
                print(f"Data uploaded to IPFS at hash: {ipfs_hash}")

            elif user_role == "patient":
                user_id = input("Enter your User ID: ")
                for record in data:
                    if record['Name'] == user_id:
                        patient_data = {
                            "User ID": record['Name'],
                            "Age": record['Age'],
                            "Blood Group": record['Blood Type'],
                            "Test Results": record['Test Results']
                        }

                        ipfs_hash = upload_to_ipfs(json.dumps(patient_data))
                        print(f"Data uploaded to IPFS at hash: {ipfs_hash}")
                        break
                else:
                    print("User ID not found.")

            time.sleep(10)
        else:
            print("Consensus failed. Cannot proceed.")

