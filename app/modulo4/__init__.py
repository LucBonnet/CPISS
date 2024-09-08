import os

from app.database.database import db

facts_file_path = os.path.join(os.path.dirname(__file__), "fatos.txt")

class Modulo4:

  def main(self):
    facts = []
    file = open(facts_file_path, "r")
    for line in file.readlines():
      fact = line.split(",")
      facts.append(fact)
    file.close()

    for fact in facts:
      fact_id, fact_value = fact
      db.connect()
      sql = "UPDATE fatos SET valor = ? WHERE id = ?"
      db.execute(sql, (fact_value,fact_id))
      db.close()