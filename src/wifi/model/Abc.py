from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import pandas as pd

# Load the health data
file_path = 'user_health_data.csv'
health_data = pd.read_csv(file_path)

# Function to encrypt data
def encrypt_data(attribute_key, plaintext):
    key = str(attribute_key).encode('utf-8')
    key = key.ljust(32, b'\0')[:32]
    iv = os.urandom(16)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext, iv

# Encrypt the health data
encrypted_data = []
for index, row in health_data.iterrows():
    attribute_key = row['Age']
    data_to_encrypt = f"{row['Name']},{row['Age']},{row['Blood Type']},{row['Admission Type']},{row['Medication']},{row['Test Results']}"
    ciphertext, iv = encrypt_data(attribute_key, data_to_encrypt)
    encrypted_data.append({
        'Name': row['Name'],
        'Encrypted Data': ciphertext.hex(),
        'IV': iv.hex()
    })

# Create a DataFrame for encrypted data
encrypted_df = pd.DataFrame(encrypted_data)

# Save to CSV
encrypted_df.to_csv('encrypted_health_data.csv', index=False)

# Display all rows of the DataFrame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("Encrypted Healthcare Data:\n")
print(encrypted_df)
print("\nHealthcare data encrypted and saved as 'encrypted_health_data.csv'\n")

