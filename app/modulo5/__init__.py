from debugpy.adapter.servers import connections
from tensorflow.python.ops.summary_ops_v2 import graph

from app.utils.randomId import generateRandomId

from app.database.database import db

from app.models.Graph import Graph


class Modulo5:
    def __init__(self):
        graphs = Graph.findByStep(5)

        if len(graphs) > 0:
            self.graph_id = graphs[0].graph_id
            return

        self.graph_id = Graph.create(5)

    def updateParticipationLevel(self, users_ids):
        sql = "UPDATE pessoas SET nivel_participacao = nivel_participacao + 1 WHERE id = ?"
        for user_id in users_ids:
            db.connect()
            db.execute(sql, (user_id,))
            db.close()

    def combine_edges_weights(self, conn1, conn2):
        print(conn1)
        print(conn2)
        newWeight = max(conn1["peso"], conn2["peso"])
        newDescription = conn1["descricao"]
        if conn2["etapa"] == 2:
            newDescription = conn2["descricao"]

        newConnection = {
            "peso": newWeight,
            "descricao": newDescription,
            "etapa": None
        }
        print(newConnection)
        return newConnection

        # return (weight1 + weight2) / 2

    def main(self):
        print("Módulo 5")

        result_conns = Graph.findByStepWithConnections()

        print(result_conns)

        # graphs = set()
        # connections = {}
        # for conn in result_conns:
        #     graphs.add(conn["id_grafo"])
        #     key = (conn["id_pessoa_a"], conn["id_pessoa_b"], conn["id_grafo"])
        #     r_key = tuple(reversed(key))
        #     if connections.get(key) is not None:
        #         print(connections[key][0], conn["peso"])
        #         new_weight = self.combine_edges_weights(connections[key][0], conn["peso"])
        #         connections[key] = (new_weight, conn["descricao"] if conn["etapa"] == 2 else connections.get(key)[1])
        #     elif connections.get(r_key) is not None:
        #         new_weight = self.combine_edges_weights(connections[r_key][0], conn["peso"])
        #         connections[r_key] = (new_weight, conn["descricao"] if conn["etapa"] == 2 else connections.get(key)[1])
        #     else:
        #         connections[key] = (conn["peso"], conn["descricao"])
        #
        #     self.updateParticipationLevel((conn["id_pessoa_a"], conn["id_pessoa_b"]))

        conns = {}
        graphs = set()
        for conn in result_conns:
            graphs.add(conn["id_grafo"])
            key = (conn["id_pessoa_a"], conn["id_pessoa_b"])
            reversed_key = (conn["id_pessoa_b"], conn["id_pessoa_a"])


            conn1 = { "peso": conn["peso"], "descricao": conn["descricao"], "etapa": conn["etapa"] }
            if not(conns.get(key) is None):
                print(conns.get(key))
                print(conn)
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

        for graph_id in graphs:
            sql = "DELETE FROM grafos WHERE id = ?"
            db.connect()
            db.execute(sql, (graph_id,))
            db.close()

        connections_ids = []
        for key, data in conns.items():
            if data["peso"] == 0:
                continue

            user_a_id, user_b_id = key

            db.connect()
            sql = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, descricao, peso, id_grafo) VALUES (?,?,?,?,?)"
            result = db.insert(sql, (user_a_id, user_b_id, data["descricao"], data["peso"], self.graph_id))
            connections_ids.append(result)
            db.close()

        return connections_ids
