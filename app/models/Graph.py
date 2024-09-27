from app.database.database import db

from app.utils.randomId import generateRandomId

class Graph():
  @staticmethod
  def create(step: int):
    sql = "INSERT INTO grafos (id, etapa) VALUES (?,?)"
    
    db.connect()
    graph_id = generateRandomId()
    db.insert(sql, (graph_id, step))
    db.close()

    return graph_id