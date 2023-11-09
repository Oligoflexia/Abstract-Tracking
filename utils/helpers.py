import pandas as pd

def populate_from_csv(csv_path:str, table_name:str):
    df = pd.read_csv(csv_path)
    pass