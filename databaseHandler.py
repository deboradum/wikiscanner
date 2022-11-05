import os
from dotenv import load_dotenv
import psycopg2

class Database:
    def __init__(self):
        load_dotenv()
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get("HOST"),
                database=os.environ.get("DATABASE"),
                user=os.environ.get("USR"),
                password=os.environ.get("PASSWD")
            )
        except Exception as e:
            print("Error connecting to database: ", e)

    def get_version(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT version()')
        data = cursor.fetchone()
        print("Connection established to: ",data)
