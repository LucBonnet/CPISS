import os

from app.database.database import db
from app.utils.randomId import generateRandomId

persons_file_path = os.path.join(os.path.dirname(__file__), "pessoas.txt")
connections_file_path = os.path.join(os.path.dirname(__file__), "conexoes.txt")
victims_file_path = os.path.join(os.path.dirname(__file__), "vitimas.txt")

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
            sql = """INSERT OR IGNORE INTO pessoas (nome, identificador) VALUES (?, ?);"""
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
        file.close()

        if len(id_pessoas) > 2:
          sql_insert_connection = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, descricao, peso, id_grafo) VALUES (?,?,?,?,?)"
          connections_file = open(connections_file_path, "r", encoding="utf-8")

          file_lines = connections_file.readlines()
          for file_line in file_lines:
            code_person_a, code_person_b, description = file_line.strip().split(";")

            sql_find_person = "SELECT id FROM pessoas WHERE identificador = ?"
            
            db.connect()
            person_a = db.execute(sql_find_person, (code_person_a,))
            db.close()
            if len(person_a) == 0:
              raise Exception(f"Erro ao criar conexão\nPessoa {code_person_a} não encontrada")
            else:
              person_a = person_a[0]

            id_pessoa_a = person_a[0]

            db.connect()
            person_b = db.execute(sql_find_person, (code_person_b,))
            db.close()
            if len(person_b) == 0:
              raise Exception(f"Erro ao criar conexão\nPessoa {code_person_b} não encontrada")
            else:
              person_b = person_b[0]

            db.connect()
            sql = """INSERT INTO grafos (id, etapa) VALUES (?,?)"""
            graph_id = generateRandomId()
            db.insert(sql, (graph_id, 2))
            db.close()

            id_pessoa_b = person_b[0]

            db.connect()
            db.insert(sql_insert_connection, (id_pessoa_a, id_pessoa_b, description, 1, graph_id))
            db.close()

          connections_file.close()
          
          victims_file = open(victims_file_path, "r", encoding="utf-8")
          file_lines = victims_file.readlines()
          for file_line in file_lines:
            code_person = file_line.strip()

            sql_find_person = "SELECT id FROM pessoas WHERE identificador = ?"
            
            db.connect()
            person = db.execute(sql_find_person, (code_person,))
            db.close()
            if len(person) == 0:
              raise Exception(f"Erro ao adicionar vítima\nPessoa {code_person} não encontrada")
            else:
              person = person[0]

            id_person = person[0]
            sql = "INSERT INTO vitimas (id_pessoa) VALUES (?)"
            db.connect()
            db.insert(sql, (id_person,))
            db.close()

          victims_file.close()

        return id_pessoas, pessoas