from app.database.database import db

from app.utils.randomId import generateRandomId

class Graph:
  def __init__(self, graph_id, step):
    self.graph_id = graph_id
    self.step = step

  @staticmethod
  def create(step: int):
    sql = "INSERT INTO grafos (id, etapa) VALUES (?,?)"
    
    db.connect()
    graph_id = generateRandomId()
    db.insert(sql, (graph_id, step))
    db.close()

    return graph_id
  
  @staticmethod
  def findByStep(step: int):
    sql = "SELECT * FROM grafos WHERE etapa = ?"
    
    db.connect()
    result = db.execute(sql, (step, ))
    db.close()

    graphs: list[Graph] = []

    if len(result) == 0:
      return graphs
    
    for graph in result:
      graphs.append(Graph(*graph))

    return graphs

  @staticmethod
  def findByStepWithConnections():
    sql = "SELECT * FROM grafos AS g INNER JOIN conexoes AS c on c.id_grafo = g.id WHERE etapa <> 5"
    
    db.connect()
    result = db.execute(sql)
    db.close()

    graphs: list[Graph] = []

    if len(result) == 0:
      return graphs
    
    for graph in result:
      graphData = {
        "id_grafo": graph[0],
        "etapa": graph[1],
        "conn_id": graph[2],
        "id_pessoa_a": graph[3],
        "id_pessoa_b": graph[4],
        "descricao": graph[5],
        "peso": graph[6],
      }

      graphs.append(graphData)

    return graphs