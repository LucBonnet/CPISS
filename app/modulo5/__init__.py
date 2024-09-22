from app.utils.randomId import generateRandomId

from app.database.database import db

class Modulo5:
  def __init__(self):
    sql = "SELECT * FROM grafos WHERE etapa = 5"
    db.connect()
    result = db.execute(sql)
    db.close()

    if len(result) > 0:
      self.graph_id = result[0][0]
      return

    self.graph_id = generateRandomId()
    db.connect()
    sql = """INSERT INTO grafos (id, etapa) VALUES (?,?)"""
    db.insert(sql, (self.graph_id, 5))
    db.close()
  
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

    sql = "SELECT c.* FROM grafos as g INNER JOIN conexoes as c on g.id = c.id_grafo WHERE g.etapa <> 5"
    db.connect()
    result_conns = db.execute(sql)
    db.close()

    # print(result_conns)

    graphs = set()
    connections = {}
    for conn_id, id_p_a, id_p_b, description, weight, graph_id in result_conns:
      graphs.add(graph_id) 
      key = (id_p_a, id_p_b, graph_id)
      r_key = tuple(reversed(key))
      if connections.get(key) != None:
        connections[key] = self.combineEdgesWeights(connections[key], weight)
      elif connections.get(r_key) != None:
        connections[r_key] = self.combineEdgesWeights(connections[r_key], weight)
      else:
        connections[key] = weight

      self.updateParticipationLevel((id_p_a, id_p_b))

    for graph_id in graphs:
      sql = "DELETE FROM grafos WHERE id = ?"
      db.connect()
      db.execute(sql, (graph_id,))
      db.close()

    connections_ids = []
    for key, new_weight in connections.items():
      if new_weight == 0:
        continue
      
      user_a_id, user_b_id, graph_id = key

      db.connect()
      sql = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, descricao, peso, id_grafo) VALUES (?,?,?,?,?)"
      result = db.insert(sql, (user_a_id, user_b_id, description, new_weight, self.graph_id))
      connections_ids.append(result)
      db.close()

    return connections_ids
