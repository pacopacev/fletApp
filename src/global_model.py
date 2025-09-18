import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv


class GlobalModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalModel, cls).__new__(cls)
            cls._instance.data = {}
        return cls._instance

    def __init__(self):
        
        load_dotenv()  # Loads from .env automatically

        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.connection = None
        self.cursor = None
        
        print(f"DB Config - Name: {self.dbname}, User: {self.user}, Host: {self.host}, Port: {self.port}")

    def set_data(self, key, value):
        """Set data globally."""
        self.data[key] = value

    def get_data(self, key):
        """Get data globally."""
        return self.data.get(key, None)

    async def connect(self):
        """Establish the database connection and create a cursor."""
        try:
            # Ensure port is an integer if not None
            port = int(self.port) if self.port is not None else None
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=port,
                cursor_factory=RealDictCursor
            )
            self.cursor = self.connection.cursor()
            # print("Database connection established successfully!")
            return True
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    async def close(self):
        """Close the cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

    async def execute_query_all(self, query, params=None):   
        if self.connection is None or self.cursor is None:
            await self.connect()  # Try to connect

        # Check again after attempting to connect
        if self.connection is None or self.cursor is None:
            print("Database connection or cursor not available. Check your .env configuration.")
            return []

        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(f"Error executing query: {e}")
            if self.connection:
                self.connection.rollback()
            return []

    def fetch_data(self, query, params=None):
        """Fetch data from the database."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
#////////////////////////////////////
    def insert_data(self, table, data, columns):
        """Universal function to insert data into any table."""
        #print(f"Data: {data}")
        #print(f"Table: {table}")

        try:
            # Ensure data is a tuple and it has the correct format (values in order)
            if not isinstance(data, tuple):
                raise ValueError("Data must be a tuple.")

            if len(data) != len(columns):
                raise ValueError("The number of data values must match the number of columns.")

            # Prepare placeholders for SQL query (e.g., %s for each value in the tuple)
            placeholders = ', '.join(['%s'] * len(data))

            # Dynamically build the SQL query, specifying columns and placeholders
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table),  # The table name
                sql.SQL(',').join(map(sql.Identifier, columns)),  # Columns to insert
                sql.SQL(placeholders)  # Placeholders for the values
            )

            # Execute the query using the data tuple
            self.execute_query_insert(query, data)

            # Commit the changes
            self.connection.commit()
            print(f"Data successfully inserted into {table} table.")

        except Exception as e:
            # Handle any exceptions
            print(f"Error inserting data into {table}: {e}")
            self.connection.rollback()



    def execute_query_insert(self, query, params=None):
        """Execute a single query (for insert queries)."""
        try:
            self.cursor.execute(query, params)
            # For INSERT, no need to return data, just execute it
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()



    def execute_query_del(self, query, params=None):
        print(query)
        print(params)
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()

    def execute_query_update(self, table: str, columns: tuple, updates: tuple, where: tuple):
        try:
            if self.connect():
                set_clause = ', '.join([f"{col} = %s" for col in columns])
                where_clause = ' AND '.join([f"{k} = %s" for k, _ in where])
                sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
                params = list(updates) + [v for _, v in where]
                self.cursor.execute(sql, params)
                self.connection.commit()
                print("✅ Update successful.")
        except Exception as e:
            print(f"[!] Error executing update: {e}")
            if self.connection:
                self.connection.rollback()
        finally:
            self.close()