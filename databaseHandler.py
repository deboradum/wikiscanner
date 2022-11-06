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

    def destroy(self):
        self.conn.close()

    def get_version(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT version()')
        data = cursor.fetchone()
        print("Connection established to: ",data)
        cursor.close()

    def insert_revision(self, revs):
        cursor = self.conn.cursor()
        rows = []
        for rev in revs:
            rev_id = rev.get("revid")
            parent_id = rev.get("parentid")
            ip = rev.get("user")
            time = rev.get("timestamp")
            comment = rev.get("comment")
            row = (rev_id, parent_id, ip, time, comment)
            rows.append(row)
        records_list = ','.join(['%s'] * len(rows))
        query = "INSERT INTO revision VALUES {}".format(records_list)

        cursor.execute(query, rows)
        cursor.close()
