from app.utils.randomId import generateRandomId

from app.database.database import db

class Modulo5:
  def __init__(self):
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

    sql = "SELECT max(id) FROM conexoes"
    db.connect()
    result = db.execute(sql)
    db.close()
    max_id = result[0][0]

    if max_id == None:
      return []

    graphs = set()
    connections = {}
    batch_size = 100
    for i in range(0, max_id, batch_size):
      sql = "SELECT * FROM conexoes WHERE id >= ? AND id < ?"
      db.connect()
      result = db.execute(sql, (i, i + batch_size))
      db.close()
      for conn in result:
        graphs.add(conn[4]) 
        key = (conn[1], conn[2])
        r_key = tuple(reversed(key))
        
        weight = conn[3]
        if connections.get(key) != None:
          self.updateParticipationLevel(key)
          connections[key] = self.combineEdgesWeights(connections[key], weight)
        elif connections.get(r_key) != None:
          self.updateParticipationLevel(r_key)
          connections[r_key] = self.combineEdgesWeights(connections[r_key], weight)
        else:
          connections[key] = weight

    for graph_id in graphs:
      sql = "DELETE FROM grafos WHERE id = ?"
      db.connect()
      db.execute(sql, (graph_id,))
      db.close()

    connections_ids = []
    for key, new_weight in connections.items():
      if new_weight == 0:
        continue
      
      user_a_id, user_b_id = key

      db.connect()
      sql = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, peso, id_grafo) VALUES (?,?,?,?)"
      result = db.insert(sql, (user_a_id, user_b_id, new_weight, self.graph_id))
      connections_ids.append(result)
      db.close()

    return connections_ids
