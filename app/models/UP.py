from typing import List, Tuple

from app.database.database import db

class UP:
  def __init__(self, up_id, document, name, np=1, f_pl=0, importance=0) -> None:
    self.up_id = up_id
    self.document = document
    self.name = name
    self.facts: List[Tuple]  = []
    self.participation_level: int = np
    self.formmated_pl: float = f_pl
    self.importance: float = importance

  def addFact(self, fact_value: float) -> None:
    if fact_value < 0 or fact_value > 1:
      raise Exception("Fato com valor inválido! Os valores dos fatos devem ser um número entre 0 e 1")

    self.facts.append(fact_value)

  def setParticipationLevel(self, value: int) -> None:
    self.participation_level = value

  def setImportance(self, value: float) -> None:
    self.importance = value

  def __repr__(self) -> str:
    return self.__str__()

  def __str__(self) -> str:
    return f"Id: {self.up_id}\nNome: {self.name}\nRG: {self.document}\nNível de participação: {self.participation_level}\nNível de participação [0,1]: {self.formmated_pl}\nImportância: {self.importance:.10f}"
  
  @staticmethod
  def create(personData):
    insert_up = "INSERT OR IGNORE INTO pessoas (nome, identificador) VALUES (?, ?);"
    select = "SELECT identificador FROM pessoas WHERE identificador = ?"
    
    data_to_insert = []
    
    if type(personData) is list:
      db.connect()
      for person in personData:
        result = db.execute(select, (person[1],))
        if len(result) == 0:
          data_to_insert.append(person)
      db.close()


      db.connect()
      db.insert(insert_up, data_to_insert)
      db.close()
    
    elif type(personData) is tuple:
      data_to_insert = [personData]

      db.connect()
      result = db.execute(select, (personData[0],))
      if len(result) == 0:
        data_to_insert.append(personData)
      db.close()

      db.connect()
      db.insert(insert_up, data_to_insert)
      db.close()

    persons = []
    for person in data_to_insert:
      person = UP.findByCode(person[1])
      persons.append(person)
      
    return persons
  
  @staticmethod
  def findByCode(code: str):
    sql = "SELECT id, identificador, nome FROM pessoas WHERE identificador = ?"
    db.connect()
    result = db.execute(sql, (code,))
    db.close()

    if len(result) == 0:
      return None

    return UP(*result[0])
  
  @staticmethod
  def getOrderByImportance(limit=None):
    sql = "SELECT * FROM pessoas ORDER BY importancia DESC"
    
    db.connect()

    if limit != None:
      sql += " LIMIT ?"
      result = db.execute(sql, (limit,))
    else:
      result = db.execute(sql)

    db.close()

    ups: list[UP] = []
    if len(result) == 0:
      return ups
    
    for up in result:
      ups.append(UP(*up))

    return ups
    
  def findById(up_id: str):
    sql = "SELECT * FROM pessoas WHERE id = ?"
    
    db.connect()
    result = db.execute(sql, (up_id,))
    db.close()

    if len(result) == 0:
      return None

    return UP(*result[0])

  def getAll():
    persons: list[UP] = []

    sql = "SELECT max(id) FROM pessoas"

    db.connect()
    result = db.execute(sql)
    db.close()
    max_id = result[0][0]

    if max_id == None:
      return persons
    
    batch_size = 100
    for i in range(0, max_id, batch_size):
      sql = "SELECT * FROM pessoas WHERE id >= ? AND id < ?"
      db.connect()
      result = db.execute(sql, (i, i + batch_size))
      db.close()

      if len(result) == 0:
        continue

      for up in result:
        persons.append(UP(*up))
    
    return persons
