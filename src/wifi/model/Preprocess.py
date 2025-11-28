import pandas as pd
import time
from sklearn.preprocessing import normalize, LabelEncoder
def normalize_data(df):
    exclude_cols = ['IoT_Node_ID', 'ip_src', 'ip_dest', 'loc_x', 'loc_y','bandwidth']
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    valid_numeric_cols = [col for col in numeric_cols if col not in exclude_cols and df[col].notnull().all()]
    if valid_numeric_cols:
        df[valid_numeric_cols] = normalize(df[valid_numeric_cols])

    categorical_cols = df.select_dtypes(include=['object']).columns
    categorical_cols = [col for col in categorical_cols if col not in exclude_cols]
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    
    return df

file_txt = 'Collected_data.txt'
df_txt = pd.read_csv(file_txt)
print(f"\n===================\n  Collected Data:\n===================\n\n", df_txt)
time.sleep(5)
normalized_df_txt = normalize_data(df_txt.copy())
normalized_df_txt.to_csv('Preprocessed_data.txt', index=False)
print(f"\n======================\n  Preprocessed Data:\n======================\n\n", normalized_df_txt)
