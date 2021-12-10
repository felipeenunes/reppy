import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(user="rodrigo", password="1234", host="localhost", port="5432")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS reppy;")
cursor.execute("CREATE DATABASE reppy;")
cursor.close()
conn.close()
conn = psycopg2.connect(database="reppy", user="rodrigo", password="1234", host="localhost", port="5432")
os.system("flask db upgrade")
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO 
        addresses(street, street_number, city, zip_code, uf)
    VALUES
        ('Rua Laurindo Borges', '3232', 'Alabama', '12312313', 'PR'),
        ('Rua Bacharel em Ciencias da Computação', '254', 'Sunday Bloody Sunday', '32524512', 'TO'),
        ('Avenida Mãe de Pet', '85', 'Também é Mãe', '53355215', 'RJ'),
        ('Avenida Alfredo Tarraga', '4658', 'Crossfit', '54545242', 'SP'),
        ('Rua Abelardo Freitas', '333', 'Cidade', '54545274', 'PR');
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
        ('Republica Sarcóphagos', 'Republica para sarcófagos e mafagafinhos', 2, 15, 400, '08/12/2021', '08/12/2021', '12345678901', 2),
        ('Republica Detran', 'Republica para detrons e detox', 1, 5, 120, '08/12/2021', '08/12/2021', '12345678902', 3),
        ('Republica Mexico Delas', 'Republica para mexicanos e guatemaltecos', 4, 11, 500, '08/12/2021', '08/12/2021', '12345678903', 4),
        ('Republica 100 Noção', 'Republica para 100s e noções', 10, 20, 720, '08/12/2021', '08/12/2021', '12345678904', 5);
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