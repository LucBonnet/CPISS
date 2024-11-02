from app.database.database import db

class Connection():
  def __init__(self, conn_id, id_person_a, id_person_b, description, weight, id_graph, step=None):
    self.conn_id = conn_id
    self.id_person_a = id_person_a
    self.id_person_b = id_person_b
    self.description = description
    self.weight = weight
    self.id_graph = id_graph
    self.step = step

  def __repr__(self) -> str:
    return self.__str__()

  def __str__(self) -> str:
    return f"{self.conn_id} -> ({self.id_person_a}, {self.id_person_b}) - {self.description}\n"


  def create(connectionData):
    sql_insert_connection = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, descricao, peso, id_grafo) VALUES (?,?,?,?,?)"
    
    connections = []
    if type(connectionData) is list:
      for conn in connectionData:
        if conn[3] == 0:
          continue
        connections.append(conn) 
        
    elif type(connectionData) is tuple:
      if connectionData[3] != 0:
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
    sql = "SELECT c.id, c.id_pessoa_A, c.id_pessoa_B, c.descricao, c.peso, c.id_grafo, g.etapa FROM conexoes AS c INNER JOIN grafos AS g on c.id_grafo = g.id WHERE ((id_pessoa_a = ? AND id_pessoa_b = ?) OR (id_pessoa_a = ? AND id_pessoa_b = ?)) AND id_grafo = ?"

    db.connect()
    result = db.execute(sql, (id_p_a, id_p_b, id_p_b, id_p_a, graph_id))
    db.close()

    connections = []
    for conn in result:
      connections.append(Connection(*conn))

    return connections

  @staticmethod
  def find_by_persons_and_step(id_p_a, id_p_b, step):
    sql = "SELECT c.id, c.id_pessoa_A, c.id_pessoa_B, c.descricao, c.peso, c.id_grafo, g.etapa FROM conexoes AS c INNER JOIN grafos AS g on c.id_grafo = g.id WHERE ((id_pessoa_a = ? AND id_pessoa_b = ?) OR (id_pessoa_a = ? AND id_pessoa_b = ?)) AND g.etapa = ?"

    db.connect()
    result = db.execute(sql, (id_p_a, id_p_b, id_p_b, id_p_a, step))
    db.close()

    if len(result) == 0:
      return None

    data = result[0]
    return Connection(*data)

  @staticmethod
  def getAll():
    connections: list[Connection] = []
    sql = "SELECT max(id) FROM conexoes"
    
    db.connect()
    result = db.execute(sql)
    db.close()
    max_id = result[0][0]

    if max_id == None:
      return connections
    
    sql = "SELECT c.id, c.id_pessoa_A, c.id_pessoa_B, c.descricao, c.peso, c.id_grafo, g.etapa FROM conexoes AS c INNER JOIN grafos AS g on c.id_grafo = g.id WHERE c.id >= ? AND c.id < ?"
    
    batch_size = 100
    for i in range(0, max_id, batch_size):
      db.connect()
      result = db.execute(sql, (i, i + batch_size))
      db.close()

      for conn in result:
        connections.append(Connection(*conn))
    
    return connections
  
  @staticmethod
  def get_all_unique():
    connections: list[dict[str, str]] = []

    sql = "SELECT DISTINCT id_pessoa_A, id_pessoa_B FROM conexoes"
    db.connect()
    result = db.execute(sql)
    db.close()

    for conn in result:
      data = {
        "id_person_a": conn[0],
        "id_person_b": conn[1],
      }
      connections.append(data)
    
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