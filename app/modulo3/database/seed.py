from database import db_policia

pessoas = [
    ('419976309', 'Carlos'),
]

fatos = [
    ('1', 'Homicídio', 'Homicídio'),
    ('2', 'Roubo a mão armada', 'Roubo a mão armada'),
]

pessoa_fato = [
    ('419976309', '1'),
    ('419976309', '2'),
]

conexoes = []

def clearData():
    db_policia.connect()

    sql = "DELETE FROM pessoas;"
    db_policia.execute(sql)

    sql = "DELETE FROM fatos;"
    db_policia.execute(sql)

    sql = "DELETE FROM pessoa_fato;"
    db_policia.execute(sql)

    sql = "DELETE FROM conexoes;"
    db_policia.execute(sql)

    sql = "DELETE FROM sqlite_sequence;"
    db_policia.execute(sql)

    db_policia.close()

def main():
    clearData()

    db_policia.connect()
    
    sql = "INSERT INTO pessoas (rg,apelido) VALUES (?,?)"
    if len(pessoas) > 0:
        db_policia.insert(sql, pessoas)

    sql = "INSERT INTO fatos (tipo,nome,descricao) VALUES (?,?,?)"
    if len(fatos) > 0:
        db_policia.insert(sql, fatos)

    sql = "INSERT INTO pessoa_fato (rg_pessoa,id_fato) VALUES (?,?)"
    if len(pessoa_fato) > 0:
        db_policia.insert(sql, pessoa_fato)

    sql = "INSERT INTO conexoes (rg_pessoa_a,rg_pessoa_b) VALUES (?,?,?)"
    if len(conexoes) > 0:
        db_policia.insert(sql, conexoes)

if __name__ == "__main__":
    main()