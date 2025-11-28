import pandas as pd


file_path = 'user_health_data.csv'
data = pd.read_csv(file_path)
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', None)  
pd.set_option('display.max_colwidth', None)  

print("\n=================\nCollected Data:\n=================\n")
print(data)

