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

    def updateParticipationLevel(self, person_id, value):
        sql = "UPDATE pessoas SET nivel_participacao = nivel_participacao + ? WHERE id = ?"
        db.connect()
        db.execute(sql, (value, person_id))
        db.close()

    def combine_edges_weights(self, conn1, conn2):
        newWeight = max(conn1["peso"], conn2["peso"])
        newDescription = conn1["descricao"]
        if conn2["etapa"] == 2:
            newDescription = conn2["descricao"]

        newConnection = {
            "peso": newWeight,
            "descricao": newDescription,
            "etapa": None
        }
        return newConnection

        # return (weight1 + weight2) / 2

    def group_connections(self, connections):
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

    def main(self):
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

    def test(self, current_state: Case, connections: list[Connection]):
        persons = current_state.persons
        result_conns = []
        for conn in connections:
            data = {
                "id_grafo": conn.id_graph,
                "etapa": 2,
                "conn_id": conn.conn_id,
                "id_pessoa_a": conn.id_person_a,
                "id_pessoa_b": conn.id_person_b,
                "descricao": conn.description,
                "peso": conn.weight,
            }
            result_conns.append(data)
        
        persons_np, new_connections, graphs = self.group_connections(result_conns)
        for person in persons:
            increment_np = 0 if persons_np.get(person.up_id) is None else persons_np.get(person.up_id)
            person.setParticipationLevel(person.participation_level + increment_np)

        graph_id = generateRandomId()
        conns = []
        for i, (key, data) in enumerate(new_connections.items()):
            if data["peso"] == 0:
                continue

            id_p_a, id_p_b = key
            conn = Connection(len(current_state.connections) + i + 1, id_p_a, id_p_b, data["descricao"], data["peso"], graph_id)
            conns.append(conn)

        print(persons)
        print(conns)

        return persons, conns
