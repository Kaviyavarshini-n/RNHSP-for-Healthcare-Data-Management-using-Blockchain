import csv
import json
import random
import time
from getpass import getpass
import requests

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

def generate_otp():
    return f"{random.randint(100000, 999999)}"

def multi_factor_authentication(user_role, password, generated_password, user_passwords):
    print(f"User role detected: {user_role}")
    otp = generate_otp()
    print(f"Generated OTP: {otp}")

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        entered_otp = input("Enter OTP: ")
        if entered_otp == otp:
            print("Authentication successful!")
            return True
        else:
            print("Invalid OTP. Please try again.")

        attempts += 1

    print("Authentication failed after 3 invalid attempts!")
    return False

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
    user_role, password, generated_password, user_passwords = get_role_and_password()
    ac = AccessControl()

    if not ac.check_permission(user_role, "read"):
        print("Access Denied!")
    else:
        if multi_factor_authentication(user_role, password, generated_password, user_passwords):
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
                print(f" data uploaded to IPFS at hash: {ipfs_hash}")

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
                        print(f" data uploaded to IPFS at hash: {ipfs_hash}")
                        break             	 
                else:
                    print("User ID not found.")

            time.sleep(10)
        else:
            print("Authentication failed. Cannot proceed.")
