import pandas as pd
import os

def load_data(file_path):
    try:
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

def save_data(df, file_path):
    df.to_csv(file_path, index=False)