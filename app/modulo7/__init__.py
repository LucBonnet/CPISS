import matplotlib.pyplot as plt
import networkx as nx

from app.database.database import db

class Modulo7:
  def __init__(self):
    self.graph = nx.Graph()

  def main(self):
    print("Módulo 7")

    sql = "SELECT max(id) FROM pessoas"
    db.connect()
    result = db.execute(sql)
    db.close()
    max_id = result[0][0]

    if max_id == None:
      return
    
    labels = {}
    batch_size = 100
    for i in range(0, max_id, batch_size):
      sql = "SELECT * FROM pessoas WHERE id >= ? AND id < ?"
      db.connect()
      result = db.execute(sql, (i, i + batch_size))
      db.close()
    
      for up in result:
        up_id, rg, name, np, importance = up
        self.graph.add_node(up_id)
        labels[up_id] = f"{rg}\n{(round(importance * 100)):.2f}%"

    sql = "SELECT max(id) FROM conexoes"
    db.connect()
    result = db.execute(sql)
    db.close()
    max_id = result[0][0]

    if max_id == None:
      return
    
    batch_size = 100
    for i in range(0, max_id, batch_size):
      sql = "SELECT * FROM conexoes WHERE id >= ? AND id < ?"
      db.connect()
      result = db.execute(sql, (i, i + batch_size))
      db.close()

      for conn in result:
        up_a_id = conn[1]
        up_b_id = conn[2]
        weight = conn[3]

        self.graph.add_edge(up_a_id, up_b_id, weight=weight)
    
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(self.graph, k=3)  
    nx.draw(self.graph, pos, with_labels=False, node_color='#2C4C7C', edge_color='#3F5BD2', font_color="#FFFFFF", node_size=2000, width=0.5)
    edge_labels = dict([((u,v,), f"{d['weight']:.2f}") for u,v,d in self.graph.edges(data=True)])
    nx.draw_networkx_labels(self.graph, pos, labels, font_color="#FFFFFF", font_size=10)
    nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)
    plt.show()
