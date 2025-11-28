import csv
import hashlib
import json
import time
from datetime import datetime
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()
        
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, str(datetime.now()), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), str(datetime.now()), new_data, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

def store_encrypted_data(blockchain, file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            blockchain.add_block(row)

def retrieve_encrypted_data(blockchain):
    for block in blockchain.chain:
        print(f"Block {block.index} [{block.timestamp}]: {block.data}\n")

if __name__ == "__main__":
    blockchain = Blockchain()
    encrypted_data_file = "encrypted_health_data.csv"
    store_encrypted_data(blockchain, encrypted_data_file)
    print("\n======================\n  Blockchain Ledger:  \n======================\n")
    time.sleep(2)
    retrieve_encrypted_data(blockchain)

