import app.database.database as db

pessoas = ['Nome1', 'Nome2', 'Nome3', 'Nome4', 'Nome5', 'Nome6', 'Nome7', 'Nome8']

class Modulo2():
    def main(self):
        db.connect()

        for pessoa in pessoas:
            sql = """INSERT INTO pessoas (nome) VALUES (?);"""
            db.execute(sql, (pessoa,))

        db.close()
        print("Modulo 2")