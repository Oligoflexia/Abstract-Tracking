from utils.operations import create_db_from_schema, drop_db, add_record, drop_table_records
from utils.dbconnections import DBConnection


if __name__ == "__main__":
    dbconnection = DBConnection('abstracts.db')
    conn = dbconnection.get_connection()
    
    #create_db_from_schema('abstracts.db', 'abstracts.sql')
    #drop_db('abstracts.db')
    
    #add_record(conn, {'first_name': 'Souvik', 'last_name': 'Maiti', 'prefix': 'Mr', 'role': 'Data Administrator'}, 'People')
    drop_table_records(conn, 'People')