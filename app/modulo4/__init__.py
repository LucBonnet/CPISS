import os

from app.models.Fact import Fact

facts_file_path = os.path.join(os.path.dirname(__file__), "fatos.txt")

class Modulo4:
  def getDataFromFile(self, file_path):
    facts = []
    if file_path:
      with open(file_path, 'r') as facts_file:
        for fact in facts_file.readlines():
          fact_type, value = fact.split(";")
          facts.append((fact_type.strip(), float(value.strip())))
    
    return facts

  def main(self, facts_file_path):
    print("Módulo 4")

    facts = self.getDataFromFile(facts_file_path)
    
    Fact.update(facts)