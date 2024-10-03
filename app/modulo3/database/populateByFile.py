from __future__ import annotations

import json

from app.modulo3.database.database import db_policia


def clear_data():
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


def populate_by_file(file_path: str | None):
    if not file_path:
        return

    file = open(file_path, "r", encoding="utf-8")
    data = json.load(file)
    file.close()

    if not data:
        return

    clear_data()

    pessoas = []
    for person in data["pessoas"]:
        person = (person["documento"], person["nome"])
        pessoas.append(person)

    fatos = []
    for fact in data["fatos"]:
        fact = (fact["tipo"], fact["nome"], fact["descricao"])
        fatos.append(fact)

    pessoa_fato = []
    for p_f in data["pessoa_fato"]:
        p_f = (p_f["documento_pessoa"], p_f["tipo_fato"])
        pessoa_fato.append(p_f)

    conexoes = []
    for conn in data["conexoes"]:
        conn = (conn["doc_pessoa_a"], conn["doc_pessoa_b"], conn["descricao"], conn["peso"])
        conexoes.append(conn)

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

    sql = "INSERT INTO conexoes (rg_pessoa_a,rg_pessoa_b,descricao,peso) VALUES (?,?,?,?)"
    if len(conexoes) > 0:
        db_policia.insert(sql, conexoes)

    db_policia.close()
