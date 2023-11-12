import pandas as pd
from utils import db_operations

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

def expand_authors_df(df: pd.DataFrame) -> pd.DataFrame:
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

# TODO: Format dates into YYYY-MM-DD
def abstract_handling(conn, df:pd.DataFrame):
    columns = ['internal_ID', 'title', 'section', 'status', 'submitter_ID', 'result', 'presentation_day', 'presentation_time']
    df['Abstract ID'] = pd.to_numeric(df['Abstract ID'], errors='coerce')
    df['Abstract ID'] = df['Abstract ID'].fillna(0).astype(int)
    

    
    df.drop(columns=['Authors'], inplace= True) 
    
    person_key_data = db_operations.get_pkeys_for_values(conn, 'People', 'person_ID', 'first_name')
    df.columns = columns
    df['submitter_ID'] = df.apply(map_cols_to_pkey, axis=1, mapping=person_key_data, column_names=['submitter_ID'])
    
    dict_list = df.to_dict('records')
    return dict_list

def authors_handling(conn, df:pd.DataFrame):
    authors = df.iloc[:, [0, 2]]
    authors.columns = ['a_id', 'Authors']
    authors = expand_authors_df(authors)
    
    person_key_data = db_operations.get_pkeys_for_values(conn, 'People', 'person_ID', 'first_name', 'last_name')
    abstract_key_data = db_operations.get_pkeys_for_values(conn, 'Abstract', 'abstract_ID', 'internal_ID')
    
    authors['p_id'] = authors.apply(map_cols_to_pkey, axis=1, mapping=person_key_data, column_names=['first_name', 'last_name'])
    authors.drop(['first_name', 'last_name'], axis=1, inplace=True)
    authors['a_id'] = authors.apply(map_cols_to_pkey, axis=1, mapping=abstract_key_data, column_names=['a_id'])
    
    return authors