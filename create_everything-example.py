import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# conn = psycopg2.connect(user="rgxvcsilpsigpr", password="3f3e6f971884c1943795dbf987bb44027efa30a230d1c06fa195ccced2cfb31a", host="ec2-54-198-213-75.compute-1.amazonaws.com", port="5432")
# conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# cursor = conn.cursor()


conn = psycopg2.connect(database="d5h6oerts2ud69", user="rgxvcsilpsigpr", password="3f3e6f971884c1943795dbf987bb44027efa30a230d1c06fa195ccced2cfb31a", host="ec2-54-198-213-75.compute-1.amazonaws.com", port="5432")
# os.system("flask db upgrade")
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

cursor.execute("""
    INSERT INTO 
        addresses(street, street_number, city, uf_id, zip_code)
    VALUES
        ('Rua Laurindo Borges', '3232', 'Alabama', 1, '12312313'),
        ('Rua Bacharel em Ciencias da Computação', '254', 'Sunday Bloody Sunday', 1, '3252451'),
        ('Avenida Mãe de Pet', '85', 'Também é Mãe', 2, '53355215'),
        ('Avenida Alfredo Tarraga', '4658', 'Crossfit', 3, '545452');
""")


cursor.execute("""
    INSERT INTO 
        users(cpf, "name", email, college, phone_number, "password_hash", address_id) 
    VALUES
        ('12345678901', 'Camilo Renato', 'camilo-renato@email.com', 'Vida', '44999999', 'senha1234', 1),
        ('12345678902', 'Aborílo Mendes', 'abmendes@email.com', 'Unespar', '44999998', 'senha1235', 1),
        ('12345678903', 'Caxias Marcondes', 'cxmarc@email.com', 'UFPG', '44999997', 'senha1236', 2),
        ('12345678904', 'Amanda Sebário', 'mandinhaseb@email.com', 'Unioeste', '44999996', 'senha1237', 3),
        ('12345678905', 'Alfredo Gostias', 'alfGostias@email.com', 'UniMacaré', '44999995', 'senha1238', 4);
""")

cursor.execute("""
    INSERT INTO
        republics ("name", description, vacancies_qty, max_occupancy, price, created_at, updated_at, user_cpf, address_id)
    VALUES
        ('Republica Kanil', 'Republica para cachorros e cachorras', 3, 10, 350, '08/12/2021', '08/12/2021', '12345678901', 1),
        ('Republica Sarcóphagos', 'Republica para sarcófagos e mafagafinhos', 2, 15, 400, '08/12/2021', '08/12/2021', '12345678901', 1),
        ('Republica Detran', 'Republica para detrons e detox', 1, 5, 120, '08/12/2021', '08/12/2021', '12345678902', 2),
        ('Republica Mexico Delas', 'Republica para mexicanos e guatemaltecos', 4, 11, 500, '08/12/2021', '08/12/2021', '12345678903', 3),
        ('Republica 100 Noção', 'Republica para 100s e noções', 10, 20, 720, '08/12/2021', '08/12/2021', '12345678904', 4);
""")

cursor.execute("""
    INSERT INTO 
        pictures (picture_url, rep_id)
    VALUES
        ('Imagem 1, republica 6', 1),
        ('Imagem 2, republica 6', 1),
        ('Imagem 1, republica 7', 2),
        ('Imagem 1, republica 8', 3),
        ('Imagem 1, republica 9', 4);
""")
            
conn.commit()
cursor.close()
conn.close()
