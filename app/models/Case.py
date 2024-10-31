from app.models.UP import UP
from app.models.Connection import Connection

class Case:
  def __init__(self):
    self.persons: list[UP] = []
    self.connections: list[Connection] = []

  def get_state(self):
    self.persons = UP.getAll()
    self.connections = Connection.getAll()