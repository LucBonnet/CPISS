import os

from app.database.database import db
from app.utils.randomId import generateRandomId

persons_file_path = os.path.join(os.path.dirname(__file__), "pessoas.txt")

class Modulo2:
    def main(self):
        print("Módulo 2")

        file = open(persons_file_path, "r")
        lines = file.readlines()

        pessoas_arquivo = []
        for line in lines:
          name, rg = line.split(",")
          pessoas_arquivo.append((name.strip(), rg.strip()))

        id_pessoas = []
        pessoas = []
        for pessoa, rg in pessoas_arquivo:
            sql = """INSERT OR IGNORE INTO pessoas (nome, rg) VALUES (?, ?);"""
            db.connect()
            id_atual = db.insert(sql, (pessoa, rg))
            db.close()
            if id_atual:
              id_pessoas.append(id_atual)

              sql = "SELECT * FROM pessoas WHERE id = ?"
              db.connect()
              p = db.execute(sql, (id_atual,))
              db.close()

              if len(p) >= 0:
                pessoas.append(p[0])

        if len(id_pessoas) > 2:
          db.connect()
          sql = """INSERT INTO grafos (id, etapa) VALUES (?,?)"""
          graph_id = generateRandomId()
          db.insert(sql, (graph_id, 2))

          sql = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, peso, id_grafo) VALUES (?,?,?,?)"
          db.insert(sql, (id_pessoas[1], id_pessoas[0], 1, graph_id))
        
          db.close()

        return id_pessoas, pessoas