from app.database.database import db

class Victim():
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