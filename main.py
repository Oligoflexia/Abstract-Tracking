import sqlite3

def create_from_schema():

    conn = sqlite3.connect('abstracts.db')
    cursor = conn.cursor()
    
    # Read the SQL file
    with open('abstracts.sql', 'r') as sql_file:
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

create_from_schema()