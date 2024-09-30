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
      db.execute(sql, (user_id, ))
      db.close()

  def combineEdgesWeights(self, weight1: float, weight2: float):
    return (weight1 + weight2) / 2

  def main(self):
    print("Módulo 5")

    result_conns = Graph.findByStepWithConnections()

    graphs = set()
    connections = {}
    for conn in result_conns:
      graphs.add(conn["id_grafo"]) 
      key = (conn["id_pessoa_a"], conn["id_pessoa_b"], conn["id_grafo"])
      r_key = tuple(reversed(key))
      if connections.get(key) != None:
        new_weight = self.combineEdgesWeights(connections[key], conn["peso"])
        connections[key] = (new_weight, conn["descricao"] if conn["etpa"] == 2 else connections.get(key)[1])
      elif connections.get(r_key) != None:
        new_weight = self.combineEdgesWeights(connections[r_key], conn["peso"])
        connections[r_key] = (new_weight, conn["descricao"] if conn["etpa"] == 2 else connections.get(key)[1])
      else:
        connections[key] = (conn["peso"], conn["descricao"])

      self.updateParticipationLevel((conn["id_pessoa_a"], conn["id_pessoa_b"]))

    for graph_id in graphs:
      sql = "DELETE FROM grafos WHERE id = ?"
      db.connect()
      db.execute(sql, (graph_id,))
      db.close()

    connections_ids = []
    for key, (new_weight, description) in connections.items():
      if new_weight == 0:
        continue
      
      user_a_id, user_b_id, graph_id = key

      db.connect()
      sql = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, descricao, peso, id_grafo) VALUES (?,?,?,?,?)"
      result = db.insert(sql, (user_a_id, user_b_id, description, new_weight, self.graph_id))
      connections_ids.append(result)
      db.close()

    return connections_ids
