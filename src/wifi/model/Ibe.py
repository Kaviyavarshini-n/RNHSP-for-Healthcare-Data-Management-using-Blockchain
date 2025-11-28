from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
import hashlib
import pandas as pd


file_path = 'user_health_data.csv'
health_data = pd.read_csv(file_path)
def derive_key(identity):
    return hashlib.sha256(identity.encode('utf-8')).digest()
def encrypt_data(identity, plaintext):
    key = derive_key(identity)
    iv = get_random_bytes(16)  
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext, iv
encrypted_data = []
for index, row in health_data.iterrows():
    identity = row['Name']  
    data_to_encrypt = f"{row['Name']},{row['Age']},{row['Blood Type']},{row['Admission Type']},{row['Medication']},{row['Test Results']}"
    ciphertext, iv = encrypt_data(identity, data_to_encrypt)
    encrypted_data.append({
        'Name': row['Name'],
        'Encrypted Data': ciphertext.hex(),
        'IV': iv.hex()
    })


encrypted_df = pd.DataFrame(encrypted_data)
encrypted_df.to_csv('encrypted_health_data_ibe.csv', index=False)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("Encrypted Healthcare Data with Identity-Based Encryption:\n")
print(encrypted_df)
print("\nHealthcare data encrypted using IBE and saved as 'encrypted_health_data_ibe.csv'\n")

