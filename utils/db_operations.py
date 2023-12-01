import os
import sqlite3
import logging
import pandas as pd


# Create operations
def create_db_from_schema(db_path: str, schema_path: str) -> int:
    """
    Creates an SQLite3 database from an SQL file containing the schema
    only if the database does not already exist.

    This function manages its own connection to the database as it should
    only ever be run to create a new database from a schema.

        Parameters:
            db_path (str): Path of the database file (currently the root directory)
            schema_path (str): Path of the SQL schema file (also currently root)

        Returns:
            (int) 1 if database is created, and -1 otherwise
    """
    # create a database if one doesn't exist
    if not os.path.exists(db_path):
        logging.info("Creating database in file: %s", db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    else:
        logging.error("Database at path: %s already exists!", db_path)
        return -1

    # Read the SQL schema file
    try:
        with open(schema_path, "r") as sql_file:
            sql_script = sql_file.read()
    except FileNotFoundError as e:
        logging.error("Schema file with path: %s not found!", schema_path)
        return -1

    # Execute the SQL to create the tables
    try:
        cursor.executescript(sql_script)
        conn.commit()
        logging.info(
            "Set up database %s from schema-file at: %s", db_path, schema_path
        )
    except sqlite3.Error as e:
        logging.error("Operation unsuccessful. Error: %s", e)
        return -1
    finally:
        cursor.close()
        conn.close()
        return 1


def add_record(
    conn: sqlite3.Connection, data_dict: dict, table_name: str
) -> int:
    cursor = conn.cursor()

    columns = ", ".join(data_dict.keys())
    placeholders = ":" + ", :".join(data_dict.keys())

    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, data_dict)

    conn.commit()
    cursor.close()


# Read operations
def record_exists(
    conn: sqlite3.Connection, table_name: str, query_params
) -> bool:
    cursor = conn.cursor()

    where_clause = " AND ".join([f"{key} = ?" for key in query_params])
    select_query = f"SELECT 1 FROM {table_name} WHERE {where_clause} LIMIT 1"

    cursor.execute(select_query, tuple(query_params.values()))
    exists = cursor.fetchone()

    cursor.close()

    return exists is not None


def get_pkeys_for_values(
    conn: sqlite3.Connection,
    query_table : str,
    key_id: str,
    *replacement_columns: str,
) -> dict:
    cursor = conn.cursor()

    columns = ", ".join(replacement_columns)
    query = f"SELECT {key_id}, {columns} FROM {query_table}"

    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    return {tuple(row[1:]): row[0] for row in data}


def get_all_fkeys(conn: sqlite3.Connection) -> dict[str:tuple]:
    SELECT = "SELECT fk.'from' AS foreign_key, m.name, fk.'to' AS reference\n"
    FROM = (
        "FROM sqlite_schema AS m,\n\tpragma_foreign_key_list(m.name) AS fk\n"
    )
    WHERE = "WHERE m.type='table';"


# Update operations


# Delete operations
def drop_db(db_name: str) -> int:
    logging.warning(
        "You're about to delete the entire database at path: %s", db_name
    )
    logging.warning(
        "Press the Y key and Enter to confirm. Any other key will cancel."
    )

    response = input("Input [Y] ?: ")

    if response.upper() == "Y":
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


def drop_all_tables(conn: sqlite3.Connection, db_name: str) -> int:
    pass


def drop_table(conn: sqlite3.Connection, table_name: str, db_name: str) -> int:
    pass


def drop_table_records(conn: sqlite3.Connection, table_name: str) -> int:
    logging.warning("You're about to delete all records in: %s", table_name)
    logging.warning(
        "Press the Y key and Enter to confirm. Any other key will cancel."
    )

    response = input("Input [Y] ?: ")

    if response.upper() == "Y":
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
        logging.info(
            "A total of %s rows were deletde from %s",
            cursor.rowcount,
            table_name,
        )
        cursor.close()
        return 1
    else:
        logging.info("exiting")


def drop_record(
    conn: sqlite3.Connection, table_name: str, db_name: str, sql: str
) -> int:
    pass


def add_abstract_records(
    conn: sqlite3.Connection, dict_list: list[dict]
) -> int:
    """
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
    """

    for dic in dict_list:
        params = {"title": dic["title"], "internal_ID": dic["internal_ID"]}

        if not record_exists(conn, "Abstract", query_params=params):
            try:
                add_record(conn, dic, "Abstract")

                logging.info("Abstract with title %s added!", dic["title"])
            except sqlite3.Error as e:
                logging.error(
                    "Ran into an error adding abstract: %s for: %s: %s",
                    dic["title"],
                    dic["presentation_day"],
                    e,
                )
        else:
            logging.error(
                "Abstract with name: %s and ID: %s already exists!",
                dic["title"],
                dic["internal_ID"],
            )


def add_attended_records():
    pass


def add_authors_records(
    conn: sqlite3.Connection, csv_records: pd.DataFrame
) -> int:
    csv_records.columns = ["a_id", "p_id"]
    dict_list = csv_records.to_dict("records")

    for dic in dict_list:
        params = {"p_id": dic["p_id"], "a_id": dic["a_id"]}
        if not record_exists(conn, "Authors", query_params=params):
            try:
                add_record(conn, dic, "Authors")
                logging.info(
                    "Record with p_id: %s, a_id: %s added!",
                    dic["p_id"],
                    dic["a_id"],
                )
            except sqlite3.Error as e:
                logging.error(
                    "Ran into an error adding p_id: %s, a_id: %s: %s",
                    dic["p_id"],
                    dic["a_id"],
                    e,
                )
        else:
            logging.error(
                "Record with p_id: %s, a_id: %s already exists!",
                dic["p_id"],
                dic["a_id"],
            )


def add_conference_records(conn: sqlite3.Connection, dict_list: list[dict]):
    for dic in dict_list:
        params = {
            "conference_name": dic["conference_name"],
            "start_date": dic["start_date"],
        }

        if not record_exists(conn, "Conferences", query_params=params):
            try:
                add_record(conn, dic, "Conferences")
                logging.info(
                    "Conference with name %s added!", dic["conference_name"]
                )
            except sqlite3.Error as e:
                logging.error(
                    "Ran into an error adding Conference: %s, error:%s",
                    dic["conference_name"],
                    e,
                )
        else:
            logging.error(
                "Conference with name: %s at date: %s already exists!",
                dic["conference_name"],
                dic["start_date"],
            )


def add_people_records(
    conn: sqlite3.Connection, csv_records: list[dict]
) -> int:
    csv_records.columns = ["first_name", "last_name", "prefix", "role"]
    dict_list = csv_records.to_dict("records")

    for dic in dict_list:
        params = {
            "first_name": dic["first_name"],
            "last_name": dic["last_name"],
        }
        if not record_exists(conn, "People", query_params=params):
            try:
                add_record(conn, dic, "People")
                logging.info(
                    "Record with name %s %s added!",
                    dic["first_name"],
                    dic["last_name"],
                )
            except sqlite3.Error as e:
                logging.error(
                    "Ran into an error adding record %s %s: %s",
                    dic["first_name"],
                    dic["last_name"],
                    e,
                )
        else:
            logging.error(
                "Record with name %s %s already exists!",
                dic["first_name"],
                dic["last_name"],
            )


def add_presented_records():
    pass


