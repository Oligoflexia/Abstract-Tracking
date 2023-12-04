import pandas as pd
from sqlite3 import Connection
import csv

from utils import db_operations

# TODO: Docstring, conference record
# def populate_from_csv(conn:Connection, csv_path:str) -> None:

#     # Handle First Author and Submitted by columns
#     first_authors = [name.split(', ')[0] for name in df['authors']]
#     first_authors_dicts = []
#     for fa in first_authors:
#         flname = fa.split(" ")
        
#         if len(flname) != 2:
#             first_authors_dicts.append({'first_name': fa, 'last_name': None})
#         else:
#             first_authors_dicts.append({'first_name': flname[0], 'last_name': flname[1]})
    
#     first_authors = pd.DataFrame(first_authors_dicts, columns=['first_name', 'last_name'])
#     person_key_data = db_operations.get_pkeys_for_values(conn, 
#                                                          'People', 'person_ID', 
#                                                          'first_name', 'last_name')
#     first_authors['first_author'] = first_authors.apply(map_cols_to_pkey, axis=1, 
#                                                         mapping=person_key_data, 
#                                                         column_names=['first_name', 
#                                                                       'last_name'])
#     first_authors.drop(['first_name', 'last_name'], axis=1, inplace=True)
#     df['first_author'] = first_authors
    
#     person_key_data = db_operations.get_pkeys_for_values(conn, 
#                                                          'People', 'person_ID', 
#                                                          'first_name')
#     df['submitter_ID'] = df.apply(map_cols_to_pkey, axis=1, 
#                                   mapping=person_key_data, column_names=['submitter_ID'])
    
#     # Make sure that the date is converted properly
#     df['presentation_day'] = pd.to_datetime(df['presentation_day'], errors='coerce')
#     df['presentation_day'] = df['presentation_day'].dt.strftime("%Y-%m-%d") 
    

def populate_from_csv(conn:Connection, csv_path: str, year:int, conf:str) -> None:
    """Populates a given database with records from a CSV file.

    Handles replacements in columns with foreign key constraints
    automatically.
    Expects proper formatting in the CSV file:
        - TODO.

    Parameters:
        - conn (Connection object): a SQLite3 connection object.
        - csv_path (str): path to a CSV containing data (in 'data/')

    Returns:
        - None

    Modifies:
        - Currently connected database.
    """
    # 1. Converts the CSV to a pd.DF
    # 2. Handle conference record creation
    # 3. Create abstracts records and insert
    
    df: pd.DataFrame = pd.read_csv(csv_path)
    columns = ['internal_ID', 'title', 'authors', 'section', 'status', 'submitter_ID',
               'result', 'presentation_day', 'presentation_time']
    
    df.columns = columns


    # Create abstracts records
    abstracts = df[['title', 'authors']]
    abstracts = abstracts.drop_duplicates(subset=['title', 'authors'])
    abstracts['summary'] = ""
    abstracts['pop_size'] = 0
    abstracts['year'] = year
    
    abstracts_dict = abstracts.to_dict('records')
    db_operations.add_abstract_records(conn, abstracts_dict)
    
    # Create conference record (if required)
    
    
    # Create People records from all people in Authors (if required)
    names = format_authors(df)
    db_operations.add_people_records(conn, names)
    
    # Insert author data
    authors_df = df.loc[:, ['internal_ID', 'authors']]
    authors = expand_authors_df(authors_df)
    authors = authors_handling(conn, authors)
    db_operations.add_authors_records(conn, authors)
    
    
    
    
    


def format_authors(df:pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame with an 'authors' column containing a list of
    strings saved as a single string and returns a DataFrame with the
    columns: 0:first_name 1:last_name 3:prefix 4:role where every unique
    name is represented
    
        Parameters:
            - df (DataFrame): a DataFrame containing 'authors' column
        
        Returns:
            - (DataFrame) with all unique names in df and 4 columns
        
        Modifies:
            - None
    """
    
    def grab_names(row):
        names = row['authors'].split(', ')
        name_tuple_list = [(name.split(" ")[0].strip(), name.split(" ")[1].strip()) 
                           for name in names if len(name.split(" ")) == 2]
        
        other_names_list = [(name.strip(),) 
                            for name in names if len(name.split(" ")) != 2]
        
        for name in name_tuple_list: name_set.add(name)
        for name in other_names_list: name_set.add(name)

    name_set = set() 

    df.apply(grab_names, axis=1)

    names = pd.DataFrame(name_set)

    names['prefix'] = None
    names['role'] = None
    
    return names

# TODO: Docstring, prompt for cases != 2
def expand_authors_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['authors'] = df['authors'].apply(lambda x: [name.strip() for name in x.split(',')])

    expanded = df.explode('authors')

    def split_name(name):
        parts = name.split()
        if len(parts) == 2:
            first_name, last_name = parts
        else:
            first_name = name
            last_name = None
        return first_name, last_name
    
    expanded[['first_name', 'last_name']] = expanded['authors'].apply(lambda x: pd.Series(split_name(x)))
    expanded.drop('authors', axis=1, inplace=True)
    
    return expanded

# TODO: docstring 
def map_cols_to_pkey(row, mapping, column_names):
    value_tuple = tuple(row[col] for col in column_names)
    return mapping.get(value_tuple)

# TODO: docstring
def authors_handling(conn, df:pd.DataFrame):
    df.columns = ['a_id', 'first_name', 'last_name']
    
    person_key_data = db_operations.get_pkeys_for_values(conn, 'People', 'person_ID', 'first_name', 'last_name')
    abstract_key_data = db_operations.get_pkeys_for_values(conn, 'Abstract', 'abstract_ID', 'internal_ID')
    
    df['p_id'] = df.apply(map_cols_to_pkey, axis=1, mapping=person_key_data, column_names=['first_name', 'last_name'])
    df.drop(['first_name', 'last_name'], axis=1, inplace=True)
    df['a_id'] = df.apply(map_cols_to_pkey, axis=1, mapping=abstract_key_data, column_names=['a_id'])
    
    return df


def write_CSV(file_path: str, tree) -> None:
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(tree["columns"])

        for row_id in tree.get_children():
            row = tree.item(row_id)['values']
            writer.writerow(row)
