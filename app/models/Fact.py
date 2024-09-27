from app.database.database import db

class Fact():
  @staticmethod
  def update(FactData):
    sql = "UPDATE fatos SET valor = ? WHERE id = ?"
    
    facts = []
    
    if type(FactData) is list:
      db.connect()
      for fact in FactData:
        f_id, value = fact
        db.execute(sql, (value, f_id))
        facts.append(fact)
      db.close()

    elif type(FactData) is tuple:
      db.connect()
      f_id, value = FactData
      db.execute(sql, (value, f_id))
      db.close()
      facts.append(FactData)

    else:
      return []
    
    db.close()

    return facts