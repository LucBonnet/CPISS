from app.database.database import db
from app.modulo3.database.database import db_policia
from app.modulo3.database.populateByFile import populate_by_file

from app.models.Graph import Graph
from app.models.Connection import Connection
from app.models.UP import UP


class Modulo3:
    def __init__(self, file=None) -> None:
        populate_by_file(file)
        self.visited_rg = set()  # Conjunto para rastrear RGs visitados

    def save_person(self, identificador):
        sql = "SELECT * FROM pessoas WHERE identificador = ?"
        db.connect()
        person = db.execute(sql, (str(identificador),))
        db.close()

        if len(person) > 0:
            return (False, person[0][0])

        sql = "SELECT rg, apelido FROM pessoas WHERE rg = ?"
        db_policia.connect()
        person = db_policia.execute(sql, (str(identificador),))[0]
        db_policia.close()

        sql = "INSERT OR REPLACE INTO pessoas (identificador, nome) VALUES (?,?)"
        db.connect()
        person_id = db.insert(sql, person)
        db.close()

        return (True, person_id)

    def find_connections(self, start_identificador, limit=50):
        """Função principal para iniciar a criação dos grafos e iteração das conexões."""
        to_visit = [start_identificador]  # Lista de RGs a serem visitados

        i = 0
        while to_visit and i < limit:
            current_rg = to_visit.pop(0)

            if current_rg not in self.visited_rg:
                result, person_a_id = self.save_person(current_rg)
                if result:
                    i += 1

                # Adicionar fatos no banco
                sql = "SELECT id_fato FROM pessoa_fato WHERE rg_pessoa = ?"
                db_policia.connect()
                result = db_policia.execute(sql, (current_rg,))
                db_policia.close()

                for fact in result:
                    fact_id = fact[0]
                    sql = "INSERT OR IGNORE INTO fatos (id) VALUES (?)"
                    db.connect()
                    db.insert(sql, (fact_id,))
                    db.close()

                    sql = "INSERT INTO pessoa_fato (id_pessoa,id_fato) VALUES (?,?)"
                    db.connect()
                    db.insert(sql, (person_a_id, fact_id))
                    db.close()

                self.visited_rg.add(str(current_rg))

                sql = "SELECT * FROM conexoes AS c INNER JOIN pessoas AS p ON c.rg_pessoa_b = p.rg WHERE rg_pessoa_a = ?"
                db_policia.connect()
                connections_with_person_b = db_policia.execute(sql, (current_rg,))
                db_policia.close()

                if len(connections_with_person_b) == 0:
                    continue

                rgs = list(map(lambda conn: conn[2], connections_with_person_b))

                # Novas conexões que serão analisadas
                connections_with_person_b = list(filter(lambda conn: conn[2] not in self.visited_rg and conn[2] not in to_visit, connections_with_person_b))
                
                # Cadastrar conexões
                for conn in connections_with_person_b:

                    if i >= limit:
                        break

                    person_b = UP.findByCode(conn[2])
                    if person_b == None:
                        person_b = UP.create((conn[6], conn[2]))[0]
                        i += 1

                    graph_id = Graph.create(3)
                    Connection.create((person_a_id, person_b.up_id, conn[3], 1, graph_id))

                newRgs = list(map(lambda conn: conn[2], connections_with_person_b))
                to_visit.extend(newRgs)

    def main(self, persons):
        print("Módulo 3")
        if len(persons) <= 0:
            return

        self.visited_rg = set() 

        for person in persons:
            self.find_connections(person)
        
# Teste da classe Modulo3
if __name__ == "__main__":
    m3 = Modulo3()
    m3.main(["1", "2"])
