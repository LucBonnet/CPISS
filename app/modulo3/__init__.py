import networkx as nx
import matplotlib.pyplot as plt

from app.database.database import db
from app.modulo3.database.database import db_policia
from app.modulo3.database.populateByFile import populateByFile
from app.utils.randomId import generateRandomId

class Modulo3:
    def __init__(self, file) -> None:
        populateByFile(file)
        self.visited_rg = set()  # Conjunto para rastrear RGs visitados

    def create_graph(self):
        """Cria um grafo de conexões e crimes para um RG específico e armazena conexões para futuros grafos."""
        sql = "INSERT INTO grafos (id, etapa) VALUES (?,?)"
        graph_id = generateRandomId()
        db.connect()
        db.insert(sql, (graph_id, 3))
        db.close()

        return graph_id

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

        sql = "INSERT OR REPLACE INTO pessoas (rg, nome) VALUES (?,?)"
        db.connect()
        person_id = db.insert(sql, person)
        db.close()

        return (True, person_id)

    def find_connections(self, start_identificador, graph_id, limit=50):
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

                sql = "SELECT * FROM conexoes WHERE rg_pessoa_a = ?"
                db_policia.connect()
                connections = db_policia.execute(sql, (current_rg,))
                db_policia.close()

                if connections == None:
                    continue

                rgs = list(map(lambda conn: conn[2], connections))

                # Novas conexões que serão analisadas
                newRgs = []
                for rg in rgs:
                    if rg not in self.visited_rg and rg not in to_visit:
                        newRgs.append(str(rg))
                
                # Cadastrar conexões
                sql = "INSERT OR REPLACE INTO conexoes (id_pessoa_A,id_pessoa_B,peso,id_grafo) VALUES (?,?,?,?)"
                for newRg in newRgs:
                    if i >= limit:
                        break
                    result, person_b_id = self.save_person(newRg)
                    if result:
                        i += 1  

                    db.connect()
                    db.insert(sql, (person_a_id, person_b_id, 1, graph_id))
                    db.close()

                to_visit.extend(newRgs)

    def main(self, persons):
        print("Módulo 3")
        if len(persons) <= 0:
            return

        self.visited_rg = set() 
        graph_id = self.create_graph()

        for person in persons:
            self.find_connections(person, graph_id)
        
# Teste da classe Modulo3
if __name__ == "__main__":
    m3 = Modulo3()
    m3.main(["1", "2"])
