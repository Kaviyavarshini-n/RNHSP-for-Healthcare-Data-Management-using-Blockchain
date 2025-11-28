import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from web3 import Web3
from solcx import install_solc, compile_source, set_solc_version

def setup_solc():
    install_solc('0.8.0')
    set_solc_version('0.8.0')

solidity_source_code ='''
pragma solidity ^0.8.0;

contract HealthcareData {
    struct Record {
        string name;
        string encryptedData;
        string iv;
    }

    Record[] public records;

    event RecordAdded(string name, string encryptedData, string iv);

    function addRecord(string memory _name, string memory _encryptedData, string memory _iv) public {
        records.push(Record(_name, _encryptedData, _iv));
        emit RecordAdded(_name, _encryptedData, _iv);
    }

    function getRecord(uint _index) public view returns (string memory, string memory, string memory) {
        require(_index < records.length, "Index out of bounds");
        Record memory record = records[_index];
        return (record.name, record.encryptedData, record.iv);
    }

    function getRecordsCount() public view returns (uint) {
        return records.length;
    }
}
'''
def compile_contract(source_code):
    setup_solc()
    compiled_sol = compile_source(
        source_code,
        output_values=['abi', 'bin'],
        solc_version='0.8.0',
    )
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_interface['abi'], contract_interface['bin']

def deploy_contract(web3, abi, bytecode, accounts):
    for account in accounts:
        print(f"Deploying contract from account: {account}")
        Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = Contract.constructor().transact({'from': account})
        print(f"Transaction hash: {tx_hash.hex()}")
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)        
        print(f"Contract deployed by {account} at address: {tx_receipt.contractAddress}\n")    
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        return contract

def load_healthcare_data(file_path):
    data = pd.read_csv(file_path)
    time.sleep(2)
    return data
    
def load_encrypt_data(file_path):
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    label_enc = LabelEncoder()
    data['Blood Type'] = label_enc.fit_transform(data['Blood Type'])
    data['Medical Condition'] = label_enc.fit_transform(data['Medical Condition'])
    data['Admission Type'] = label_enc.fit_transform(data['Admission Type'])
    data['Medication'] = label_enc.fit_transform(data['Medication'])
    data['Test Results'] = label_enc.fit_transform(data['Test Results'])
    processed_data = data[['Age', 'Blood Type', 'Medical Condition', 'Admission Type']]
    time.sleep(2)
    return processed_data

def sfs_fwzic_weight_calculation(data):
    criteria = ['Age', 'Blood Type', 'Medical Condition', 'Admission Type']
    expert_evaluations = {
        'Age': [4, 5, 5, 4, 5],
        'Blood Type': [3, 3, 4, 2, 3],
        'Medical Condition': [5, 5, 5, 4, 5],
        'Admission Type': [4, 4, 5, 4, 4],
    }
    fuzzy_scale = {
        1: (0.15, 0.85, 0.1),
        2: (0.25, 0.75, 0.2),
        3: (0.55, 0.50, 0.25),
        4: (0.75, 0.25, 0.2),
        5: (0.85, 0.15, 0.1)
    }
    fuzzy_matrix = {}
    for criterion, evaluations in expert_evaluations.items():
        fuzzy_matrix[criterion] = [fuzzy_scale[eval] for eval in evaluations]

    average_fuzzy_values = {}
    for criterion, values in fuzzy_matrix.items():
        avg_mu = np.mean([v[0] for v in values])
        avg_v = np.mean([v[1] for v in values])
        avg_pi = np.mean([v[2] for v in values])
        average_fuzzy_values[criterion] = (avg_mu, avg_v, avg_pi)
        
    def defuzzify(fuzzy_num):
        mu, v, pi = fuzzy_num
        return (mu - pi)**2 - (v - pi)**2

    crisp_weights = {criterion: defuzzify(fuzzy) for criterion, fuzzy in average_fuzzy_values.items()}
    total_weight = sum(crisp_weights.values())
    normalized_weights = {criterion: weight / total_weight for criterion, weight in crisp_weights.items()}
    print("\n=======================================\n  Calculated Weights using SFS-FWZIC:\n=======================================\n")
    time.sleep(2)
    print(normalized_weights)
    return np.array(list(normalized_weights.values()))

def grey_topsis_ranking(data, weights):
    try:
        weighted_data = data * weights
        pis = np.max(weighted_data, axis=0)
        nis = np.min(weighted_data, axis=0)
        distance_to_pis = np.sqrt(np.sum((weighted_data - pis) ** 2, axis=1))
        distance_to_nis = np.sqrt(np.sum((weighted_data - nis) ** 2, axis=1))
        closeness_coeff = distance_to_nis / (distance_to_pis + distance_to_nis)
        ranking = np.argsort(closeness_coeff)[::-1]
        return ranking, closeness_coeff

    except Exception as e:
        print(f"Error in grey_topsis_ranking: {str(e)}")
        return None, None
        
def store_data_on_blockchain(data, web3, contract):
    account = web3.eth.defaultAccount
    for index, row in data.iterrows():
        name = row['Name']    
        encrypted_data = row['Encrypted Data']
        iv = row['IV']
        try:
            tx_hash = contract.functions.addRecord(name, encrypted_data, iv).transact({'from': account})
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Record for {name} added to blockchain. Transaction Hash: {tx_hash.hex()}")
        except Exception as e:
            print(f"Error adding record for {name}: {e}")

def retrieve_data_from_blockchain(contract, index):
    try:
        record = contract.functions.getRecord(index).call()
        print(f"Record {index}: Name={record[0]}, Encrypted Data={record[1]}, IV={record[2]}\n")
    except Exception as e:
        print(f"Error retrieving record {index}: {e}")

def main():
    file_path = 'user_health_data.csv'
    health_data = load_healthcare_data(file_path)
    processed_data = preprocess_data(health_data)
    time.sleep(5)
    weights = sfs_fwzic_weight_calculation(processed_data)
    time.sleep(5)
    encrypt_file = 'encrypted_health_data.csv'
    data = load_encrypt_data(encrypt_file)
    ranking, closeness_coeff = grey_topsis_ranking(processed_data, weights)
    
    if ranking is not None:
        print("\n======== Ranking and Closeness Coefficients for 100 Users ========\n")
        time.sleep(2)
        print(f"{'User':<10}{'Rank':<10}{'Closeness Coefficient':<20}")
        print("=" * 40)
        for user_id, (rank, coeff) in enumerate(zip(ranking, closeness_coeff)):
            print(f"{user_id + 1:<10}{rank:<10}{coeff:<20.6f}")
            time.sleep(0.1)  # Optional: Adds a slight delay to simulate loading
    
    
    time.sleep(5)
    ganache_url = "HTTP://127.0.0.1:7545" 
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    if web3.is_connected():
        print("\nConnected to Ganache")
    else:
        print("\nFailed to connect to Ganache")
        return

    accounts = web3.eth.accounts
    web3.eth.defaultAccount = accounts[0]
    abi, bytecode = compile_contract(solidity_source_code)
    time.sleep(2)
    print("\n========================\n  Deploying Contracts:\n========================\n")
    time.sleep(2)
    for account in accounts:
        web3.eth.defaultAccount = account
        contract = deploy_contract(web3, abi, bytecode, [account])

    time.sleep(2)
    print("\n=================================\n  Storing Data into Blockchain:\n=================================\n")
    time.sleep(2)
    store_data_on_blockchain(data, web3, contract)
    time.sleep(2)
    print("\n====================================\n  Retrieving Data from Blockchain:\n====================================\n")
    time.sleep(2)
    for i in range (100):
    	retrieve_data_from_blockchain(contract, i)

if __name__ == "__main__":
    main()
