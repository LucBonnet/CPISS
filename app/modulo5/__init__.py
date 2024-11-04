import copy

from app.database.database import db
from app.models.Graph import Graph
from app.models.Connection import Connection
from app.models.Case import Case
from app.models.UP import UP

from app.utils.randomId import generateRandomId

class Modulo5:
    def __init__(self, print_data=True):
        self.print_data = print_data
        graphs = Graph.findByStep(5)

        if len(graphs) > 0:
            self.graph_id = graphs[0].graph_id
            return

        self.graph_id = Graph.create(5)

    def setParticipationLevel(self, person_id, value):
        sql = "UPDATE pessoas SET nivel_participacao = ? WHERE id = ?"
        db.connect()
        db.execute(sql, (value, person_id))
        db.close()

    def updateParticipationLevel(self, person_id, value):
        sql = "UPDATE pessoas SET nivel_participacao = nivel_participacao + ? WHERE id = ?"
        db.connect()
        db.execute(sql, (value, person_id))
        db.close()

    def combine_edges_weights(self, conn1, conn2):
        new_weight = max(conn1["peso"], conn2["peso"])
        desc1 = conn1["descricao"]
        desc2 = conn2["descricao"]
        new_description = f"{desc1};{desc2}"

        newConnection = {
            "peso": new_weight,
            "descricao": new_description,
            "etapa": None
        }
        return newConnection

        # return (weight1 + weight2) / 2

    def group_connections1(self, connections):
        conns = {}
        graphs = set()
        persons_np = {}
        for conn in connections:
            graphs.add(conn["id_grafo"])
            key = (conn["id_pessoa_a"], conn["id_pessoa_b"])
            reversed_key = (conn["id_pessoa_b"], conn["id_pessoa_a"])

            conn1 = { "peso": conn["peso"], "descricao": conn["descricao"], "etapa": conn["etapa"] }
            if not(conns.get(key) is None):
                conn2 = {
                    "peso": conns.get(key)["peso"],
                    "descricao": conns.get(key)["descricao"],
                    "etapa": conns.get(key)["etapa"],
                }
                newConn = self.combine_edges_weights(conn1, conn2)
                conns[key] = newConn
            elif not(conns.get(reversed_key) is None):
                conn2 = {
                    "peso": conns.get(reversed_key)["peso"],
                    "descricao": conns.get(reversed_key)["descricao"],
                    "etapa": conns.get(reversed_key)["etapa"],
                }
                newConn = self.combine_edges_weights(conn1, conn2)
                conns[reversed_key] = newConn
            else:
                conns[key] = conn1

            id_p_a = conn["id_pessoa_a"]
            id_p_b = conn["id_pessoa_b"]

            persons_np[id_p_a] = 1 if persons_np.get(id_p_a) is None else persons_np.get(id_p_a) + 1
            persons_np[id_p_b] = 1 if persons_np.get(id_p_b) is None else persons_np.get(id_p_b) + 1

        return persons_np, conns, graphs


    def main1(self):
        print("Módulo 5")

        result_conns = Graph.findByStepWithConnections()
        persons_np, new_connections, graphs = self.group_connections(result_conns)

        for person_id, increment_np in persons_np.items():
            self.updateParticipationLevel(person_id, increment_np)

        for graph_id in graphs:
            Graph.delete_by_id(graph_id)

        connections_ids = []
        for key, data in new_connections.items():
            if data["peso"] == 0:
                continue

            id_p_a, id_p_b = key
            conn = Connection.create((id_p_a, id_p_b, data["descricao"], data["peso"], self.graph_id))
            connections_ids += [c.conn_id for c in conn]

        return connections_ids

    def group_connections(self, connections):
        conns = {}
        persons_np = {}
        for conn in connections:
            key = (conn.id_person_a, conn.id_person_b)
            reversed_key = (conn.id_person_b, conn.id_person_a)

            conn1 = { "peso": conn.weight, "descricao": conn.description, "etapa": conn.step }
            if not(conns.get(key) is None):
                conn2 = {
                    "peso": conns.get(key)["peso"],
                    "descricao": conns.get(key)["descricao"],
                    "etapa": conns.get(key)["etapa"],
                }
                newConn = self.combine_edges_weights(conn1, conn2)
                conns[key] = newConn
            elif not(conns.get(reversed_key) is None):
                conn2 = {
                    "peso": conns.get(reversed_key)["peso"],
                    "descricao": conns.get(reversed_key)["descricao"],
                    "etapa": conns.get(reversed_key)["etapa"],
                }
                newConn = self.combine_edges_weights(conn1, conn2)
                conns[reversed_key] = newConn
            else:
                conns[key] = conn1
            
            id_p_a = conn.id_person_a
            id_p_b = conn.id_person_b

            persons_np[id_p_a] = 1 if persons_np.get(id_p_a) is None else persons_np.get(id_p_a) + 1
            persons_np[id_p_b] = 1 if persons_np.get(id_p_b) is None else persons_np.get(id_p_b) + 1

        return persons_np, conns

    def create_final_connections(self, connections):
        sql = "DELETE FROM conexoes_finais"
        db.connect()
        db.execute(sql)
        db.close()

        for key, data in connections.items():
            if data["peso"] == 0:
                continue
            
            id_p_a, id_p_b = key
            sql = "INSERT INTO conexoes_finais (id_pessoa_A, id_pessoa_B, descricao, peso) VALUES (?,?,?,?)"
            db.connect()
            db.insert(sql, (id_p_a, id_p_b, data["descricao"], data["peso"]))
            db.close()

    def main(self):
        print("Módulo 5")

        connections = Connection.getAll()
        
        persons_np, conns = self.group_connections(connections)

        for person_id, new_np in persons_np.items():
            self.setParticipationLevel(person_id, new_np)

        self.create_final_connections(conns)
        

    def test(self, persons, connections):        
        persons_np, unique_conns = self.group_connections(connections)
        
        for person in persons:
            new_np = persons_np.get(person.up_id) if persons_np.get(person.up_id) is not None else 0
            person.setParticipationLevel(new_np)
            
        return persons, unique_conns
