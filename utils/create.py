import sqlite3

def from_schema(db_path, schema_path):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read the SQL file
    with open(schema_path, 'r') as sql_file:
        sql_script = sql_file.read()
    
    try:
        cursor.executescript(sql_script)
        conn.commit()
        print("SQL script executed successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()