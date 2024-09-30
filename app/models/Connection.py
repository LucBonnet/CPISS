from app.database.database import db

class Connection():
  def __init__(self, conn_id, id_person_a, id_person_b, description, weight, id_graph):
    self.conn_id = conn_id
    self.id_person_a = id_person_a
    self.id_person_b = id_person_b
    self.description = description
    self.weight = weight
    self.id_graph = id_graph

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