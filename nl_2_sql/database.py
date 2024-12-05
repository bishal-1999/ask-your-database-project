import sqlite3

####################################################################################################################################

def connect_to_database():
    """Connect to SQLite database"""
    try:
        # Change the database path to your SQLite database file
        connection = sqlite3.connect("fancy_tshirts.db")  # Replace with the correct path
        return connection
    except sqlite3.Error as e:
        print(f"Error while connecting to sqlite: {e}")
        return None


####################################################################################################################################

def fetch_schema(connection):
    schema = {}
    try:
        cursor = connection.cursor()
        
        # Get list of tables from sqlite_master
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Iterate over each table and get columns
        for (table_name,) in tables:
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema[table_name] = [column[1] for column in columns]  # column[1] is the column name
        
        return schema
    except sqlite3.Error as e:
        print(f"Error fetching schema: {e}")
        return None
    finally:
        cursor.close()



####################################################################################################################################

def run_query(connection, sql_query):
    """Run SQL query against SQLite database"""
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None


####################################################################################################################################