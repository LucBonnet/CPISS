import matplotlib.pyplot as plt
import networkx as nx

class Modulo5:
  def __init__(self, *graphs) -> None:
    if len(graphs) == 0:
      self.graph = nx.Graph()
    else:
      initial_graph = nx.Graph()

      for graph in graphs:
        edge_data = {
          e: Modulo5.combineEdgesWeights(graph.edges[e]["weight"], initial_graph.edges[e]["weight"]) for e in graph.edges & initial_graph.edges
        }
        initial_graph = nx.compose(initial_graph, graph)
        nx.set_edge_attributes(initial_graph, edge_data, "weight")
      
      self.graph = initial_graph
  
  @staticmethod
  def combineEdgesWeights(weight1: float, weight2: float):
    return (weight1 + weight2) / 2
  
  def combine(self, *graphs):
    temp_graph = self.graph

    for graph in graphs:
        edge_data = {
          e: Modulo5.combineEdgesWeights(graph.edges[e]["weight"], temp_graph.edges[e]["weight"]) for e in graph.edges & temp_graph.edges
        }
        print(edge_data)
        temp_graph = nx.compose(temp_graph, graph)
        nx.set_edge_attributes(temp_graph, edge_data, "weight")
      
    self.graph = temp_graph
  
    return self.graph

def test():
  G = nx.Graph()

  G_nodes = ["A", "B", "C", "D"]
  for node in G_nodes:
    G.add_node(node)

  G.add_edge("A", "B", weight=0.5)
  G.add_edge("B", "C", weight=0.1)
  G.add_edge("A", "C", weight=0.9)
  G.add_edge("C", "D", weight=0.3)

  H = nx.Graph()

  H_nodes = ["A", "C", "E", "F"]
  for node in H_nodes:
    H.add_node(node)

  H.add_edge("C", "A", weight=0.7)
  H.add_edge("E", "F", weight=0.4)
  H.add_edge("E", "A", weight=0.2)
  H.add_edge("C", "D", weight=0.6)

  m5 = Modulo5()

  combined = m5.combine(G, H)

  plt.figure(figsize=(6, 6))
  pos = nx.spring_layout(combined, k=3)  
  nx.draw(combined, pos, with_labels=True, node_color='#2C4C7C', edge_color='#3F5BD2', font_color="#FFFFFF", node_size=250, width=0.5)
  edge_labels = dict([((u,v,), f"{d['weight']:.2f}") for u,v,d in combined.edges(data=True)])
  nx.draw_networkx_edge_labels(combined, pos, edge_labels)
  plt.show()

test()