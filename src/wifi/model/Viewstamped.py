import csv
import json
import random
import time
from getpass import getpass
import requests

class ReplicaNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data_store = {}
        self.is_leader = False
        self.view_number = 0

    def write_data(self, key, value):
        self.data_store[key] = value
        return f"Data written to replica {self.node_id}."

    def read_data(self, key):
        return self.data_store.get(key, None)

    def synchronize(self, data_store):
        self.data_store = data_store

class ViewstampedReplication:
    def __init__(self):
        self.replicas = [ReplicaNode(i) for i in range(5)]
        self.current_leader = self.replicas[0]  # Initial leader
        self.current_leader.is_leader = True

    def view_change(self):
        print("Leader failed. Initiating view change...")
        self.current_leader.is_leader = False
        self.current_leader.view_number += 1

        # Elect a new leader (round-robin)
        new_leader_id = (self.current_leader.node_id + 1) % len(self.replicas)
        self.current_leader = self.replicas[new_leader_id]
        self.current_leader.is_leader = True
        print(f"New leader is Replica {self.current_leader.node_id}, View: {self.current_leader.view_number}")

    def write(self, key, value):
        print("Writing data to replicas...")
        for replica in self.replicas:
            replica.write_data(key, value)
        return "Data written to all replicas."

    def read(self, key):
        print("Reading data from replicas...")
        # Perform quorum-based read
        data = [replica.read_data(key) for replica in self.replicas]
        return next((d for d in data if d is not None), "Data not found.")

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

def get_role_and_password():
    valid_roles = ["admin", "doctor", "patient"]
    while True:
        user_role = input("Enter your role (admin/doctor/patient): ").lower()
        if user_role not in valid_roles:
            print("Wrong choice. Please enter a valid role (admin/doctor/patient).")
            continue

        if user_role in ["admin", "doctor"]:
            password = generate_random_password()
            print(f"Generated password for {user_role}: {password}")
        elif user_role == "patient":
            password = generate_random_password()
            print(f"Generated password for patient: {password}")
        else:
            print("Invalid role!")
            continue

        entered_password = getpass("Enter password: ")
        if entered_password == password:
            print("Password is valid.")
            return user_role
        else:
            print("Invalid password. Try again.")

def generate_random_password():
    return f"{random.randint(100000, 999999)}"

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

if __name__ == "__main__":
    user_data_file = 'user_health_data.csv'
    data = load_user_data(user_data_file)
    vr = ViewstampedReplication()
    ac = AccessControl()

    user_role = get_role_and_password()

    if not ac.check_permission(user_role, "read"):
        print("Access Denied!")
    else:
        print("Access Granted!")
        time.sleep(3)

        if user_role == "admin":
            vr.write("health_data", data)
            print("Admin wrote data to replicas.")
            ipfs_hash = upload_to_ipfs(json.dumps(data))
            print(f"Data uploaded to IPFS at hash: {ipfs_hash}")

        elif user_role == "doctor":
            doctor_records = [
                {
                    "User ID": record['Name'],
                    "Medical Condition": record['Medical Condition'],
                    "Test Results": record['Test Results']
                }
                for record in data
            ]
            vr.write("doctor_data", doctor_records)
            print("Doctor wrote data to replicas.")
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
                    vr.write(f"patient_data_{user_id}", patient_data)
                    print(f"Patient {user_id} wrote data to replicas.")
                    ipfs_hash = upload_to_ipfs(json.dumps(patient_data))
                    print(f"Data uploaded to IPFS at hash: {ipfs_hash}")
                    break
            else:
                print("User ID not found.")

