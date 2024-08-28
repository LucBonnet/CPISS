import app.database.database as db

pessoas = [('Nome1'), ('Nome2'), ('Nome3'), ('Nome4')]

class Modulo2():
    def main(self):
        print("Módulo 2")
        db.connect()

        id_pessoas = []
        for pessoa in pessoas:
            sql = """INSERT INTO pessoas (nome) VALUES (?);"""
            id_atual = db.insert(sql, (pessoa,))
            id_pessoas.append(id_atual)
        db.close()

        return id_pessoas