from app.database.database import db

class Connection():
  def __init__(self, conn_id, id_person_a, id_person_b, description, weight, id_graph):
    self.conn_id = conn_id
    self.id_person_a = id_person_a
    self.id_person_b = id_person_b
    self.description = description
    self.weight = weight
    self.id_graph = id_graph

  def __repr__(self) -> str:
    return self.__str__()

  def __str__(self) -> str:
    return f"{self.conn_id} -> ({self.id_person_a}, {self.id_person_b}) - {self.description}\n"


  def create(connectionData):
    sql_insert_connection = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, descricao, peso, id_grafo) VALUES (?,?,?,?,?)"
    
    connections = []
    if type(connectionData) is list:
      for conn in connectionData:
        connections.append(conn) 
        
    elif type(connectionData) is tuple:
      connections.append(connectionData)

    else: 
      return []
    
    db.connect()
    db.insert(sql_insert_connection, connections)
    db.close()

    conns = []
    for c in connections:
      conn = Connection.find(c[0], c[1], c[4])
      conns += conn

    return conns

  @staticmethod
  def find(id_p_a, id_p_b, graph_id):
    sql = "SELECT * FROM conexoes WHERE ((id_pessoa_a = ? AND id_pessoa_b = ?) OR (id_pessoa_a = ? AND id_pessoa_b = ?)) AND id_grafo = ?"

    db.connect()
    result = db.execute(sql, (id_p_a, id_p_b, id_p_b, id_p_a, graph_id))
    db.close()

    connections = []
    for conn in result:
      connections.append(Connection(*conn))

    return connections

  
  def getAll():
    connections: list[Connection] = []
    sql = "SELECT max(id) FROM conexoes"
    
    db.connect()
    result = db.execute(sql)
    db.close()
    max_id = result[0][0]

    if max_id == None:
      return connections
    
    sql = "SELECT * FROM conexoes WHERE id >= ? AND id < ?"
    
    batch_size = 100
    for i in range(0, max_id, batch_size):
      db.connect()
      result = db.execute(sql, (i, i + batch_size))
      db.close()

      for conn in result:
        connections.append(Connection(*conn))
    
    return connections

  def delete(self):
    sql = "DELETE FROM conexoes WHERE id = ?"
    db.connect()
    db.execute(sql, (self.conn_id, ))
    db.close()

  @staticmethod
  def delete_ruido():
    sql = "DELETE FROM conexoes WHERE descricao = 'Ruído'"
    db.connect()
    db.execute(sql)
    db.close()

  def toJSON(self):
    data = {
      "id": self.conn_id,
      "id_person_a": self.id_person_a,
      "id_person_b": self.id_person_b,
      "description": self.description,
      "weight": self.weight,
      "id_graph": self.id_graph,
    }

    return data