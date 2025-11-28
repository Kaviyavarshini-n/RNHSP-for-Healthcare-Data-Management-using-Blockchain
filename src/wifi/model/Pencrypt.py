from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import serialization, hashes
import pandas as pd

# Generate RSA keys for Predicate Encryption
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Serialize public and private keys
def serialize_key(key, is_private=False):
    if is_private:
        return key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    else:
        return key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

# Encrypt data using public key and attribute-based predicates
def encrypt_with_predicate(public_key, predicate, data):
    # Combine predicate into the data to simulate a PE scenario
    combined_data = f"{predicate}:{data}".encode('utf-8')
    ciphertext = public_key.encrypt(
        combined_data,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext

# Decrypt data using private key
def decrypt_with_predicate(private_key, ciphertext):
    decrypted_data = private_key.decrypt(
        ciphertext,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted_data.decode('utf-8')

# Load the health data
file_path = 'user_health_data.csv'
health_data = pd.read_csv(file_path)

# Generate RSA keys for Predicate Encryption
private_key, public_key = generate_rsa_key_pair()

# Serialize keys for future use
private_key_pem = serialize_key(private_key, is_private=True)
public_key_pem = serialize_key(public_key)

# Save keys to files
with open('private_key.pem', 'wb') as priv_file:
    priv_file.write(private_key_pem)

with open('public_key.pem', 'wb') as pub_file:
    pub_file.write(public_key_pem)

# Encrypt the health data
encrypted_data = []
for index, row in health_data.iterrows():
    # Use 'Age' as the predicate
    predicate = str(row['Age'])
    data_to_encrypt = f"{row['Name']},{row['Age']},{row['Blood Type']},{row['Admission Type']},{row['Medication']},{row['Test Results']}"
    ciphertext = encrypt_with_predicate(public_key, predicate, data_to_encrypt)
    encrypted_data.append({
        'Name': row['Name'],
        'Encrypted Data': ciphertext.hex(),
        'Predicate': predicate,
    })

# Create a DataFrame for encrypted data
encrypted_df = pd.DataFrame(encrypted_data)

# Save to CSV
encrypted_df.to_csv('predicate_encrypted_health_data.csv', index=False)

# Display all rows of the DataFrame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("Predicate Encrypted Healthcare Data:\n")
print(encrypted_df)
print("\nHealthcare data encrypted and saved as 'predicate_encrypted_health_data.csv'\n")

