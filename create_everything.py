import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(user="user", password="1234", host="localhost", port="5432")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS reppy;")
cursor.execute("CREATE DATABASE reppy;")
cursor.close()
conn.close()
conn = psycopg2.connect(database="reppy", user="user", password="1234", host="localhost", port="5432")
os.system("flask db upgrade")
cursor = conn.cursor()
cursor.execute("""
                INSERT INTO states(UF)
                VALUES
                    ('AC'),
                    ('AL'),
                    ('AP'),
                    ('AM'),
                    ('BA'),
                    ('CE'),
                    ('DF'),
                    ('ES'),
                    ('GO'),
                    ('MA'),
                    ('MT'),
                    ('MS'),
                    ('MG'),
                    ('PA'),
                    ('PB'),
                    ('PR'),
                    ('PE'),
                    ('PI'),
                    ('RJ'),
                    ('RN'),
                    ('RS'),
                    ('RO'),
                    ('RR'),
                    ('SC'),
                    ('SP'),
                    ('SE'),
                    ('TO');
            """)
            
conn.commit()
cursor.close()
conn.close()