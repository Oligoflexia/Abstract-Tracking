from utils import db_operations, dbconnections


if __name__ == "__main__":
    
    db_operations.create_db_from_schema("abstracts.db", "abstracts.sql")
    
    dbconnection = dbconnections.DBConnection('abstracts.db')
    
    try:
        conn = dbconnection.get_connection()
        
        #db_operations.drop_db("abstracts.db")
        # db_operations.drop_table_records(conn, 'Abstract')
        # db_operations.drop_table_records(conn, 'People')
        # db_operations.drop_table_records(conn, 'Authors')
       
        
    
    finally:
        dbconnection.close_connection()