import os
import sqlite3
import logging
import pandas as pd
from utils.helpers import format_authors, expand_df, map_cols_to_pkey

# Create operations

def create_db_from_schema(db_path:str, schema_path:str) -> int:
    '''
    Creates an SQLite3 database from an SQL file containing the schema 
    if the database does not already exist.
    
    This function manages its own connection to the database as it should
    only ever be run to create a new database from a schema. 
    
        Parameters:
            db_path (str): Path of the database file (currently the root directory)
            schema_path (str): Path of the SQL schema file (also currently root)
        
        Returns:
            (int) 1 if database is created, and -1 otherwise
    '''
    # create a database if one doesn't exist
    if not os.path.exists(db_path):
        logging.info('Creating database in file: %s', db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    else:
        logging.error('Database at path: %s already exists!', db_path)
        return -1
    
    # Read the SQL schema file
    try:
        with open(schema_path, 'r') as sql_file:
            sql_script = sql_file.read()
    except FileNotFoundError as e:
        logging.error('Schema file with path: %s not found!', schema_path)
        return -1
    
    # Execute the SQL to create the tables
    try:
        cursor.executescript(sql_script)
        conn.commit()
        logging.info('Set up database %s from schema-file at: %s', db_path, schema_path)
    except sqlite3.Error as e:
        logging.error('Operation unsuccessful. Error: %s', e)
        return -1
    finally:
        cursor.close()
        conn.close()
        return 1


def add_record(conn:sqlite3.Connection, data_dict:dict, table_name:str) -> int:
    cursor = conn.cursor()
    
    columns = ', '.join(data_dict.keys())
    placeholders = ':' + ', :'.join(data_dict.keys())
    
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, data_dict)
    
    conn.commit()
    cursor.close()


def add_abstract_records(conn:sqlite3.Connection, csv_records:pd.DataFrame) -> int:
    columns = ['internal_ID', 'title', 'section', 'status', 'submitter_ID', 'result', 'presentation_day', 'presentation_time']
    csv_records['Abstract ID'] = pd.to_numeric(csv_records['Abstract ID'], errors='coerce')
    csv_records['Abstract ID'] = csv_records['Abstract ID'].fillna(0).astype(int)
    
    names = format_authors(csv_records)
    add_people_records(conn, names)
    
    authors = csv_records.iloc[:, [0, 2]]
    authors.columns = ['a_id', 'Authors']
    csv_records.drop(columns=['Authors'], inplace= True) 
    
    person_key_data = get_pkeys_for_values(conn, 'People', 'person_ID', 'first_name')
    csv_records.columns = columns
    csv_records['submitter_ID'] = csv_records.apply(map_cols_to_pkey, axis=1, mapping=person_key_data, column_names=['submitter_ID'])
    
    dict_list = csv_records.to_dict('records')
    
    for dic in dict_list:
        params = {'title': dic['title'], 'presentation_day': dic['presentation_day']}
        if not record_exists(conn, 'Abstract', query_params=params):
            try:
                add_record(conn, dic, 'Abstract')
                logging.info("Abstract with title %s added!", dic['title'])
            except sqlite3.Error as e:
                logging.error("Ran into an error adding abstract: %s for: %s: %s", dic['title'], dic['presentation_day'], e)
        else:
            logging.error("Abstract with name: %s at time: %s already exists!", dic['title'], dic['presentation_day'])
    
    person_key_data = get_pkeys_for_values(conn, 'People', 'person_ID', 'first_name', 'last_name')
    abstract_key_data = get_pkeys_for_values(conn, 'Abstract', 'abstract_ID', 'internal_ID')
    
    authors = expand_df(authors)
    authors['p_id'] = authors.apply(map_cols_to_pkey, axis=1, mapping=person_key_data, column_names=['first_name', 'last_name'])
    authors.drop(['first_name', 'last_name'], axis=1, inplace=True)
    authors['a_id'] = authors.apply(map_cols_to_pkey, axis=1, mapping=abstract_key_data, column_names=['a_id'])
    add_authors_records(conn, authors)

def add_people_records(conn:sqlite3.Connection, csv_records:pd.DataFrame) -> int:
    csv_records.columns = ['first_name', 'last_name', 'prefix', 'role']
    dict_list = csv_records.to_dict('records')
    
    for dic in dict_list:
        params = {'first_name': dic['first_name'], 'last_name': dic['last_name']}
        if not record_exists(conn, 'People', query_params=params):
            try:
                add_record(conn, dic, 'People')
                logging.info("Record with name %s %s added!", dic['first_name'], dic['last_name'])
            except sqlite3.Error as e:
                logging.error("Ran into an error adding record %s %s: %s", dic['first_name'], dic['last_name'], e)
        else:
            logging.error("Record with name %s %s already exists!", dic['first_name'], dic['last_name'])

def add_authors_records(conn:sqlite3.Connection, csv_records:pd.DataFrame) -> int:
    csv_records.columns = ['a_id','p_id']
    dict_list = csv_records.to_dict('records')
    
    for dic in dict_list:
        params = {'p_id': dic['p_id'], 'a_id': dic['a_id']}
        if not record_exists(conn, 'Authors', query_params=params):
            try:
                add_record(conn, dic, 'Authors')
                logging.info("Record with p_id: %s, a_id: %s added!", dic['p_id'], dic['a_id'])
            except sqlite3.Error as e:
                logging.error("Ran into an error adding p_id: %s, a_id: %s: %s", dic['p_id'], dic['a_id'], e)
        else:
            logging.error("Record with p_id: %s, a_id: %s already exists!", dic['p_id'], dic['a_id'])

# Read operations
def record_exists(conn:sqlite3.Connection, table_name:str, query_params) -> bool:
    cursor = conn.cursor()
    
    where_clause = ' AND '.join([f"{key} = ?" for key in query_params])
    select_query = f"SELECT 1 FROM {table_name} WHERE {where_clause} LIMIT 1"
    
    cursor.execute(select_query, tuple(query_params.values()))
    exists = cursor.fetchone()
    
    cursor.close()
    
    return exists is not None

def get_pkeys_for_values(conn: sqlite3.Connection, query_table: str, key_id: str, *replacement_columns: str) -> dict:
    cursor = conn.cursor()
    
    columns = ', '.join(replacement_columns)
    query = f"SELECT {key_id}, {columns} FROM {query_table}"
    
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    return {tuple(row[1:]): row[0] for row in data}

# Update operations


# Delete operations
def drop_db(db_name:str) -> int:
    logging.warning("You're about to delete the entire database at path: %s", db_name)
    logging.warning("Press the Y key and Enter to confirm. Any other key will cancel.")
    
    response = input("Input [Y] ?: ")
    
    if response.upper() == 'Y':

        if os.path.exists(db_name):
            
            try:
                os.remove(db_name)
                logging.info("Database at path: %s has been deleted", db_name)
                return 1
            except Exception as e:
                logging.error("Error occured during deletion process: %s", e)
                return -1
            
        else:
            logging.error("No databse found at given path: %s", db_name)
            return -1
        
    else:
        logging.info("Exiting without any deletion.")
        return 0

def drop_all_tables(conn:sqlite3.Connection, db_name:str) -> int:
    pass

def drop_table(conn:sqlite3.Connection, table_name:str, db_name:str) -> int:
    pass

def drop_table_records(conn:sqlite3.Connection, table_name:str) -> int:
    logging.warning("You're about to delete all records in: %s", table_name)
    logging.warning("Press the Y key and Enter to confirm. Any other key will cancel.")
    
    response = input("Input [Y] ?: ")
    
    if response.upper() == 'Y':
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
        logging.info("A total of %s rows were deletde from %s", cursor.rowcount, table_name)
        cursor.close()
        return 1
    else:
        logging.info("exiting")
    
    

def drop_record(conn:sqlite3.Connection, table_name:str, db_name:str, sql:str) -> int:
    pass