from app.database.database import db
from app.utils.randomId import generateRandomId

pessoas = [('Nome1', '1'), ('Nome2', '7'), ('Nome3', '8'), ('Nome4', '9')]

class Modulo2():
    def main(self):
        print("Módulo 2")
        db.connect()
        sql = """INSERT INTO grafos (id, etapa) VALUES (?,?)"""
        graph_id = generateRandomId()
        db.insert(sql, (graph_id, 2))

        id_pessoas = [1, 2, 3, 4]
        for pessoa, rg in pessoas:
            sql = """INSERT INTO pessoas (nome, rg) VALUES (?, ?);"""
            id_atual = db.insert(sql, (pessoa, rg))
            id_pessoas.append(id_atual)

        sql = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, peso, id_grafo) VALUES (?,?,?,?)"
        
        db.insert(sql, (id_pessoas[1], id_pessoas[0], 1, graph_id))

        db.close()

        return id_pessoas, pessoas