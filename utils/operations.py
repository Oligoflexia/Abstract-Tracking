import os
import sqlite3
import logging
import pandas as pd

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
    
def add_abstract_records(csv_records:pd.DataFrame) -> int:
    columns = ['internal_ID', 'title', 'section', 'status', 'result', 'first_author', 'submitter_ID', 'presentation_day', 'presentation_time']
    
    pass

def add_people_records(conn:sqlite3.Connection, csv_records:pd.DataFrame) -> int:
    csv_records.columns = ['first_name', 'last_name', 'prefix', 'role']
    dict_list = csv_records.to_dict()
    
    for dic in dict_list:
        params = {'first_name': dic['first_name'], 'last_name': dic['last_name']}
        if not record_exists(conn, 'People', params):
            try:
                add_record(conn, dic, 'People')
                logging.info("Record with name %s %s added!", dic['first_name'], dic['last_name'])
            except sqlite3.Error as e:
                logging.error("Ran into an error adding record %s %s: %s", dic['first_name'], dic['last_name'], e)
        else:
            logging.error("Record with name %s %s already exists!", dic['first_name'], dic['last_name'])
            
# Read operations
def record_exists(conn:sqlite3.Connection, table_name:str, **query_params) -> bool:
    cursor = conn.cursor()
    
    where_clause = ' AND '.join([f"{key} = ?" for key in query_params])
    select_query = f"SELECT 1 FROM {table_name} WHERE {where_clause} LIMIT 1"
    
    cursor.execute(select_query, tuple(query_params.values()))
    exists = cursor.fetchone()
    
    cursor.close()
    
    return exists is not None

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

def drop_record(conn:sqlite3.Connection, table_name:str, db_name:str, sql:str) -> int:
    pass