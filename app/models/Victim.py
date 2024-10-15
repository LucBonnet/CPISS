from app.database.database import db

class Victim():
  def __init__(self, person_id):
    self.person_id = person_id

  def create(victimData):
    sql = "INSERT INTO vitimas (id_pessoa) VALUES (?)"
    
    victims = []
    
    if type(victimData) is list:
      for victim in victimData:
        victims.append(victim)

    elif type(victimData) is tuple:
      victims.append(victimData)

    elif type(victimData) is int:
      victims.append((victimData, ))

    else:
      return []
    
    db.connect()
    db.insert(sql, victims)
    db.close()

    return victims
  
  def getAll():
    db.connect()
    sql = "SELECT * FROM vitimas"
    result_victims = db.execute(sql)
    db.close()

    victims = []
    for result in result_victims:
      victims.append(Victim(*result))
    
    return victims

  def toJSON(self):
    data = {
      "id": self.person_id
    }

    return data