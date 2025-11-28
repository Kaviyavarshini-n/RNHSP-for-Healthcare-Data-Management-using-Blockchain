import os
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import pandas as pd
import json


def derive_key(attributes, policy):
    key_material = "".join(f"{k}={v}" for k, v in attributes.items() if policy.get(k) == v)
    return key_material[:32].ljust(32, '0').encode('utf-8')  


def encrypt_data(attributes, policy, plaintext):
    try:
        key = derive_key(attributes, policy)
        iv = get_random_bytes(16)  
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        return ciphertext, iv
    except ValueError as e:
        return None, str(e)

file_path = 'user_health_data.csv'
health_data = pd.read_csv(file_path)
policy = {"Admission Type": "Emergency"}
encrypted_data = []
for index, row in health_data.iterrows():
    attributes = {"Age": row['Age'], "Admission Type": row['Admission Type']}
    plaintext = f"{row['Name']},{row['Age']},{row['Blood Type']},{row['Admission Type']},{row['Medication']},{row['Test Results']}"
    ciphertext, iv_or_error = encrypt_data(attributes, policy, plaintext)
    encrypted_data.append({
        'Name': row['Name'],
        'Ciphertext': ciphertext.hex() if ciphertext else "",
    })

encrypted_df = pd.DataFrame(encrypted_data)
encrypted_df.to_csv('encrypted_health_data_simulated_cpabe.csv', index=False)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print("Encrypted Healthcare Data with Simulated CP-ABE:\n")
print(encrypted_df)
print("\nHealthcare data encrypted using simulated CP-ABE and saved as 'encrypted_health_data_simulated_cpabe.csv'\n")

