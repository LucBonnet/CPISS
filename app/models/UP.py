from typing import List, Tuple

class UP:
  def __init__(self, up_id, name, np=1) -> None:
    self.up_id = up_id
    self.name = name
    self.facts: List[Tuple]  = []
    self.participation_level: int = np
    self.importance: float = 0

  def addFact(self, fact_name: str, fact_value: float) -> None:
    if fact_value < 0 or fact_value > 1:
      raise Exception("Fato com valor inválido! Os valores dos fatos devem ser um número entre 0 e 1")

    self.facts.append((fact_name, fact_value))

  def setParticipationLevel(self, value: int) -> None:
    self.participation_level = value

  def setImportance(self, value: float) -> None:
    self.importance = value

  def __repr__(self) -> str:
    return self.__str__()

  def __str__(self) -> str:
    return self.name + ": " + str(self.facts)
    