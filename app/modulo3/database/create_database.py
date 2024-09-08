import os

from database import db_policia

DATABASE = 'database_police.db'

def create():
    path = os.path.dirname(os.path.realpath(__file__))
    if DATABASE in os.listdir(path):
        os.remove(os.path.join(path, DATABASE))

    db_policia.connect()

    sql = """
        CREATE TABLE IF NOT EXISTS pessoas (
            rg varchar(255) primary key,
            apelido text
        );
    """
    
    db_policia.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS fatos (
            id integer primary key AUTOINCREMENT,
            tipo integer,
            nome varchar(255),
            descricao text
        );
    """
    
    db_policia.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS pessoa_fato (
            id integer primary key AUTOINCREMENT,
            rg_pessoa integer,
            id_fato integer,
            FOREIGN KEY (rg_pessoa) REFERENCES pessoas(rg) ON DELETE CASCADE
            FOREIGN KEY (id_fato) REFERENCES fatos(id) ON DELETE CASCADE
        );
    """
    
    db_policia.execute(sql)


    sql = """
        CREATE TABLE IF NOT EXISTS conexoes (
            id integer primary key AUTOINCREMENT,
            rg_pessoa_a integer,
            rg_pessoa_b integer,
            FOREIGN KEY (rg_pessoa_a) REFERENCES pessoas(rg) ON DELETE CASCADE
            FOREIGN KEY (rg_pessoa_b) REFERENCES pessoas(rg) ON DELETE CASCADE
        );
    """

    db_policia.execute(sql)

    db_policia.close()

create()