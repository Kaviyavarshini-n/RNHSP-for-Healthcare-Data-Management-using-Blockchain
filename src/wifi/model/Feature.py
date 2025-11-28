import pandas as pd
import numpy as np
import time
data = pd.read_csv('Preprocessed_data.txt')
columns_to_drop = ['ip_src', 'ip_dest']
data = data.drop(columns=columns_to_drop, axis=1)
data['byte_ratio'] = data['src_bytes'] / (data['dst_bytes'] + 1e-5)
data['log_duration'] = data['duration'].apply(lambda x: np.log(x + 1))
data['failed_logins_ratio'] = data['num_failed_logins'] / (data['logged_in'] + 1e-5)
data['bytes_interaction'] = data['src_bytes'] * data['dst_bytes']
data['protocol_type'] = data['protocol_type'].astype('category').cat.codes
data['service'] = data['service'].astype('category').cat.codes
data['flag'] = data['flag'].astype('category').cat.codes
extracted_features = data[['byte_ratio', 'log_duration', 'failed_logins_ratio', 
                           'bytes_interaction', 'protocol_type', 'service', 'flag']]

print("\n=======================\n  Extracted Features: \n=======================\n")
time.sleep(2)
print(extracted_features.head())
extracted_features.to_csv('Processed_IoT_data.csv', index=False)
