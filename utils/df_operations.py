import logging
import sqlite3
import pandas as pd
from utils import helpers, db_operations

# TODO: first_author
def add_abstract_records(conn:sqlite3.Connection, csv_records:pd.DataFrame) -> int:
    '''
    Creates new records in the database corresponding to every row in a 
    provided pd.DataFrame object. Handles insertions for values refering
    to other tables [Authors, Submitted by]
    
    Expects colums in the following [index] and (type) with arbitrary "name"
    
        [0] (int) "internal_ID"
        [1] (str) "Title"
        [2] (str) "Authors" -- names separated by ', '
        [3] (str) "Section"
        [4] (str) "Status" -- in ['Submitted', 'Draft', 'Draft Collection', 'Draft Analysis']
        [5] (str) "Submitted by" -- "firstname lastname" 
        [6] (str) "Result"
        [7] (str) "Presentation Day" -- accepts some range of date, but DD-MM-YYYY pref.
        [8] (str) "Presentation Time" -- HH:MM-HH:MM format
    
    Handles the insertion of any Authors in [2] which are not present in
    the database, populates the Authors table to track authorship, and 
    replaces the name in [5] to represent person_ID in People
    '''
    
    names = helpers.format_authors(csv_records)
    add_people_records(conn, names)
    
    authors_df = csv_records.copy()
    
    dict_list = helpers.abstract_handling(conn, csv_records)
    
    for dic in dict_list:
        
        params = {'title': dic['title'], 'internal_ID': dic['internal_ID']}
        
        if not db_operations.record_exists(conn, 'Abstract', query_params=params):
            try:
                db_operations.add_record(conn, dic, 'Abstract')

                logging.info("Abstract with title %s added!", dic['title'])
            except sqlite3.Error as e:
                logging.error("Ran into an error adding abstract: %s for: %s: %s", dic['title'], dic['presentation_day'], e)
        else:
            logging.error("Abstract with name: %s and ID: %s already exists!", dic['title'], dic['internal_ID'])
            print(dic['submitter_ID'])
    
    authors = helpers.authors_handling(conn, authors_df)
    add_authors_records(conn, authors)
    
def add_attended_records():
    pass

def add_authors_records(conn:sqlite3.Connection, csv_records:pd.DataFrame) -> int:
    csv_records.columns = ['a_id','p_id']
    dict_list = csv_records.to_dict('records')
    
    for dic in dict_list:
        params = {'p_id': dic['p_id'], 'a_id': dic['a_id']}
        if not db_operations.record_exists(conn, 'Authors', query_params=params):
            try:
                db_operations.add_record(conn, dic, 'Authors')
                logging.info("Record with p_id: %s, a_id: %s added!", dic['p_id'], dic['a_id'])
            except sqlite3.Error as e:
                logging.error("Ran into an error adding p_id: %s, a_id: %s: %s", dic['p_id'], dic['a_id'], e)
        else:
            logging.error("Record with p_id: %s, a_id: %s already exists!", dic['p_id'], dic['a_id'])

def add_conference_records():
    pass

def add_people_records(conn:sqlite3.Connection, csv_records:pd.DataFrame) -> int:
    csv_records.columns = ['first_name', 'last_name', 'prefix', 'role']
    dict_list = csv_records.to_dict('records')
    
    for dic in dict_list:
        params = {'first_name': dic['first_name'], 'last_name': dic['last_name']}
        if not db_operations.record_exists(conn, 'People', query_params=params):
            try:
                db_operations.add_record(conn, dic, 'People')
                logging.info("Record with name %s %s added!", dic['first_name'], dic['last_name'])
            except sqlite3.Error as e:
                logging.error("Ran into an error adding record %s %s: %s", dic['first_name'], dic['last_name'], e)
        else:
            logging.error("Record with name %s %s already exists!", dic['first_name'], dic['last_name'])

def add_presented_records():
    pass

