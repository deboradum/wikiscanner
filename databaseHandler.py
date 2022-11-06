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

    def insert_tags(self, revs):
        cursor = self.conn.cursor()
        rows = []
        for rev in revs:
            rev_id = rev.get("revid")
            tags = rev.get("tags")
            for tag in tags:
                row = (rev_id, tag)
                rows.append(row)
        records_list = ','.join(['%s'] * len(rows))
        query = "INSERT INTO tags VALUES {} ON CONFLICT DO NOTHING".format(records_list)
        try:
            cursor.execute(query, rows)
        except Exception as e:
            print("Error inserting: ", e)
        self.conn.commit()
        cursor.close()

    def insert_revision(self, revs):
        cursor = self.conn.cursor()
        rows = []
        for rev in revs:
            rev_id = rev.get("revid")
            parent_id = rev.get("parentid")
            ip_addr = rev.get("user")
            time = rev.get("timestamp")
            comment = rev.get("comment")
            page_id = rev.get("page_id")
            page_title = rev.get("page_title")
            row = (rev_id, parent_id, ip_addr, time, comment, page_title, page_id)
            rows.append(row)
        records_list = ','.join(['%s'] * len(rows))
        query = "INSERT INTO revision VALUES {} ON CONFLICT DO NOTHING".format(records_list)

        try:
            cursor.execute(query, rows)
        except Exception as e:
            print("Error inserting: ", e)
        self.conn.commit()
        cursor.close()

        self.insert_tags(revs)

    def insert_ip(self, ips_info):
        cursor = self.conn.cursor()
        rows = []
        for ip in ips_info:
            ip_addr = ip.get("ip")
            network = ip.get("network")
            country = ip.get("country")
            region = ip.get("region")
            city = ip.get("city")
            latitude = ip.get("latitude")
            longitude = ip.get("longitude")
            asn = ip.get("asn")
            organization = ip.get("org")
            row = (ip_addr, network, country, region, city, latitude, longitude, asn, organization)
            rows.append(row)
        records_list = ','.join(['%s'] * len(rows))
        query = "INSERT INTO ip_info VALUES {} ON CONFLICT DO NOTHING".format(records_list)

        try:
            cursor.execute(query, rows)
        except Exception as e:
            print("Error inserting: ", e)
        self.conn.commit()
        cursor.close()
