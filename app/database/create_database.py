import os

from app.database.database import db

def create():
    path = os.path.dirname(os.path.realpath(__file__))
    if "database.db" in os.listdir(path):
        os.remove(os.path.join(path, 'database.db'))

    db.connect()

    sql = """
        CREATE TABLE IF NOT EXISTS grafos (
            id integer primary key,
            etapa integer
        );
    """
    db.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS pessoas (
            id integer primary key AUTOINCREMENT,
            rg varchar(255) unique,
            nome varchar(255),
            nivel_participacao float default 1,
            importancia float default 0
        );
    """
    db.execute(sql)


    sql = """
        CREATE TABLE IF NOT EXISTS pessoa_fato (
            id integer primary key AUTOINCREMENT,
            id_pessoa integer,
            valor float,
            FOREIGN KEY (id_pessoa) REFERENCES pessoas(id) ON DELETE CASCADE
        );
    """

    db.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS conexoes (
            id integer PRIMARY KEY AUTOINCREMENT,
            id_pessoa_A integer,
            id_pessoa_B integer,
            peso float default 1,
            id_grafo integer,
            FOREIGN KEY (id_pessoa_A) REFERENCES pessoas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_pessoa_B) REFERENCES pessoas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_grafo) REFERENCES grafos(id) ON DELETE CASCADE,
            UNIQUE (id_pessoa_A, id_pessoa_B, id_grafo)
        );
    """

    db.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS preferencias (
            id_pessoa integer primary key,
            valores text,
            FOREIGN KEY (id_pessoa) REFERENCES pessoas(id)
        );
    """

    db.execute(sql)

    db.close()