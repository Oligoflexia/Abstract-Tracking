import pandas as pd

def populate_from_csv(csv_path:str, table_name:str):
    df = pd.read_csv(csv_path)
    pass

def format_authors(df):
    def grab_names(row):
        names = row['Authors'].split(', ')
        name_tuple_list = [(name.split(" ")[0].strip(), name.split(" ")[1].strip()) for name in names if len(name.split(" ")) == 2]
        other_names_list = [(name.strip(), ) for name in names if len(name.split(" ")) != 2]
        for name in name_tuple_list: name_set.add(name)
        for name in other_names_list: name_set.add(name)

    name_set = set() 

    df.apply(grab_names, axis=1)

    names = pd.DataFrame(name_set)

    names['prefix'] = None
    names['role'] = None
    
    return names

def expand_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Authors'] = df['Authors'].apply(lambda x: [name.strip() for name in x.split(',')])

    expanded = df.explode('Authors')

    def split_name(name):
        parts = name.split()
        if len(parts) == 2:
            first_name, last_name = parts
        else:
            first_name = name
            last_name = None
        return first_name, last_name
    
    expanded[['first_name', 'last_name']] = expanded['Authors'].apply(lambda x: pd.Series(split_name(x)))
    expanded.drop('Authors', axis=1, inplace=True)
    
    return expanded
    
def map_cols_to_pkey(row, mapping, column_names):
    value_tuple = tuple(row[col] for col in column_names)
    return mapping.get(value_tuple)