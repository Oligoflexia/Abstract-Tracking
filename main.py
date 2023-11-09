from utils.operations import create_db_from_schema, drop_db


if __name__ == "__main__":
    create_db_from_schema('abstracts.db', 'abstracts.sql')
    
    
