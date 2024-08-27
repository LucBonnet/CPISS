import os

import database as db

os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database.db'))

db.connect()

sql = """
    CREATE TABLE IF NOT EXISTS grafo (
        id integer primary key AUTOINCREMENT,
        etapa integer
    );
"""
db.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS pessoas (
        id integer primary key AUTOINCREMENT,
        nome varchar(255),
        nivel_participacao float default 1,
        importancia float default 0
    );
"""
db.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS fatos (
        id integer primary key AUTOINCREMENT,
        nome varchar(255)
    );
"""
db.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS pessoa_fato (
        id_pessoa integer,
        id_fato integer,
        FOREIGN KEY (id_pessoa) REFERENCES pessoas(id),
        FOREIGN KEY (id_fato) REFERENCES fatos(id)
    );
"""

db.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS conexoes (
        id_pessoa_A integer,
        id_pessoa_B integer,
        peso float default 1,
        id_grafo integer,
        FOREIGN KEY (id_pessoa_A) REFERENCES pessoas(id),
        FOREIGN KEY (id_pessoa_B) REFERENCES pessoas(id),
        FOREIGN KEY (id_grafo) REFERENCES grafo(id)
    );
"""

db.execute(sql)

db.close()