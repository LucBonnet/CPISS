import os

from app.database.database import db
from app.utils.randomId import generateRandomId

persons_file_path = os.path.join(os.path.dirname(__file__), "pessoas.txt")

class Modulo2:
    def main(self):
        print("Módulo 2")

        file = open(persons_file_path, "r")
        lines = file.readlines()

        pessoas = []
        for line in lines:
          name, rg = line.split(",")
          pessoas.append((name, rg))

        db.connect()
        id_pessoas = []
        for pessoa, rg in pessoas:
            sql = """INSERT OR IGNORE INTO pessoas (nome, rg) VALUES (?, ?);"""
            id_atual = db.insert(sql, (pessoa, rg))
            id_pessoas.append(id_atual)
        db.close()

        if len(id_pessoas) > 2:
          db.connect()
          sql = """INSERT INTO grafos (id, etapa) VALUES (?,?)"""
          graph_id = generateRandomId()
          db.insert(sql, (graph_id, 2))

          sql = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, peso, id_grafo) VALUES (?,?,?,?)"
          db.insert(sql, (id_pessoas[1], id_pessoas[0], 1, graph_id))
        
          db.close()

        return id_pessoas, pessoas