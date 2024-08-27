import networkx as nx

from UP import UP

class Modulo6:
  def __init__(self, graph: nx.Graph) -> None:
    self.graph = graph
    self.omega = 0

  def __setOmega(self):
    max_degree = 0
    degrees_sum = 0
    for node in self.graph.nodes:
      degree = self.graph.degree[node]
      if degree > max_degree:
        max_degree = degree
      degrees_sum += degree
    
    avg_degress = degrees_sum / len(self.graph.nodes)
    self.omega = 1 - (avg_degress / (max_degree * 1.1))

  def __setNP(self):
    max_np = 0
    participations_level = []
    for node, attr in self.graph.nodes(data=True):
      current_np = attr["data"].participation_level
      
      if current_np > max_np:
        max_np = current_np
      
      participations_level.append(current_np)

    for node, attr in self.graph.nodes(data=True):
      current_np = attr["data"].participation_level
      new_fact = current_np / max_np
      attr["data"].facts.append(new_fact)

  def __p(self, facts):
    mult = 1
    for f in facts:
      mult *= 1 - (f * self.omega)
    return 1 - mult

  def calcImportance(self):
    self.__setOmega()
    self.__setNP()

    for node, attr in self.graph.nodes(data=True):
      current_facts = attr["data"].facts
      attr["data"].importance = self.__p(current_facts)

def test():
  ups = [
    UP("1", "Nome UP1", 2),
    UP("2", "Nome UP2", 1),
    UP("3", "Nome UP3", 3),
    UP("4", "Nome UP4", 2),
    UP("5", "Nome UP5", 1),
  ]

  G = nx.Graph()

  for node in ups:
    G.add_node(node.up_id, data=node)
  
  for node, attr in G.nodes(data=True):
    print(attr["data"])

  G.add_edge("1", "2", weight=0.5)
  G.add_edge("2", "3", weight=0.1)
  G.add_edge("1", "3", weight=0.9)
  G.add_edge("3", "4", weight=0.3)
  G.add_edge("4", "5", weight=0.2)

  m6 = Modulo6(G)
  m6.calcImportance()

  for node, attr in G.nodes(data=True):
    print(attr["data"].importance)

test()