import networkx as nx

from app.database.database import db
from app.models.UP import UP

class Modulo6:
  def __init__(self):
    self.omega = 0

  def getNodesDegrees(self):
    sql = "SELECT max(id) FROM conexoes"
    db.connect()
    result = db.execute(sql)
    db.close()
    max_id = result[0][0]

    degrees = {}

    if max_id == None:
      return degrees
    
    batch_size = 100
    for i in range(0, max_id, batch_size):
      sql = "SELECT * FROM conexoes WHERE id >= ? AND id < ?"
      db.connect()
      result = db.execute(sql, (i, i + batch_size))
      db.close()
      for conn in result:
        up_a_id = conn[1]
        if degrees.get(up_a_id) == None:
          degrees[up_a_id] = 1
        else:
          degrees[up_a_id] += 1
        
        up_b_id = conn[2]
        if degrees.get(up_b_id) == None:
          degrees[up_b_id] = 1
        else:
          degrees[up_b_id] += 1
    
    return degrees

  def __calcNP(self, np_value, max_np):
    return np_value / max_np

  def __calcOmega(self, degrees):
    degrees_sum = sum(degrees)
    max_degree = max(degrees)

    avg_degress = degrees_sum / len(degrees)    
    return 1 - (avg_degress / (max_degree * 1.1))

  def __setOmega(self):
    degrees = self.getNodesDegrees()
    values = list(degrees.values())

    if len(values) > 0:
      self.omega = self.__calcOmega(values)
      print(f"w = {self.omega}")
    
  def __updateNP(self, ups_ids, ups_np, max_np):
    sql = "UPDATE pessoas SET np_formatado = ? WHERE id = ?"
    
    db.connect()
    for i, up_id in enumerate(ups_ids):
      np_value = self.__calcNP(ups_np[i], max_np)
      db.insert(sql, (np_value, up_id))
    db.close()

  def __setNP(self):
    sql = "SELECT max(id) FROM pessoas"
    db.connect()
    result = db.execute(sql)
    db.close()
    max_id = result[0][0]

    np = 0
    if max_id == None:
      return np
    
    max_np = 0
    ups_ids = []
    ups_np = []
    batch_size = 100
    for i in range(0, max_id, batch_size):
      sql = "SELECT * FROM pessoas WHERE id >= ? AND id < ?"
      db.connect()
      result = db.execute(sql, (i, i + batch_size))
      db.close()

      for up in result:
        up_id = up[0]
        ups_ids.append(up_id) 
        np = up[3]
        ups_np.append(np)
         
        if np > max_np:
          max_np = np

    self.__updateNP(ups_ids, ups_np, max_np)

  def __p(self, facts):
    mult = 1
    for f in facts:
      if not f == None:
        mult *= 1 - (f * self.omega)
    return (1 - mult)

  def main(self):
    print("Módulo 6")
    self.__setOmega()
    self.__setNP()

    sql = "SELECT id FROM pessoas ORDER BY id"
    db.connect()
    result = db.execute(sql)
    db.close()

    print(result)

    for up_id, in result:
      sql = "SELECT * FROM pessoa_fato WHERE id_pessoa = ?"

      db.connect()
      result = db.execute(sql, (up_id,))
      db.close()

      facts = []
      for person_fact in result:
        fact_id = person_fact[2]
        sql = "SELECT valor FROM fatos WHERE id = ?"
        db.connect()
        value = db.execute(sql, (fact_id,))[0][0]
        db.close()
        facts.append(value)
      
      sql = "SELECT * FROM pessoas WHERE id = ?"

      db.connect()
      result = db.execute(sql, (up_id,))
      db.close()

      if len(result) > 0:
        person = UP(*result[0])
        facts.append(person.formmated_pl)
      
      importance = self.__p(facts)

      sql = "UPDATE pessoas SET importancia = ? WHERE id = ?"

      db.connect()
      result = db.execute(sql, (importance,up_id))
      db.close()

      







    