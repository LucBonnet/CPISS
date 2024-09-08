from database import db_policia

pessoas = [
    ('1', 'João'),
    ('2', 'Pedro'),
    ('3', 'André'),
    ('4', 'Jorge'),
    ('5', 'Francisco'),
]

fatos = [
    ('1', 'Fato do tipo 1', 'Descrição do fato do tipo 1'),
    ('2', 'Fato do tipo 2', 'Descrição do fato do tipo 2'),
    ('3', 'Fato do tipo 3', 'Descrição do fato do tipo 3'),
]

pessoa_fato = [
    ('1', '1'),
    ('1', '2'),
    ('2', '1'),
]

conexoes = [
    ('1', '2'),
    ('1', '3'),
    ('2', '1'),
    ('3', '1'),
    ('3', '4'), 
    ('4', '1'), 
    ('4', '3'), 
    ('4', '5'), 
    ('5', '4'), 
]

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
    db_policia.insert(sql, pessoas)

    sql = "INSERT INTO fatos (tipo,nome,descricao) VALUES (?,?,?)"
    db_policia.insert(sql, fatos)

    sql = "INSERT INTO pessoa_fato (rg_pessoa,id_fato) VALUES (?,?)"
    db_policia.insert(sql, pessoa_fato)

    sql = "INSERT INTO conexoes (rg_pessoa_a,rg_pessoa_b) VALUES (?,?,?)"
    db_policia.insert(sql, conexoes)
    


if __name__ == "__main__":
    main()