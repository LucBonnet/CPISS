from typing import List
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import math
import os

from Inception_V3 import Inception_V3

IMAGES_PATH = os.path.join(os.path.dirname(__file__), '..', 'Imagens_usuarios', 'Generalist961')
USERS_PATH = os.path.join(os.path.dirname(__file__), '..', 'Imagens_usuarios', 'users_data')

model = Inception_V3()
print("Modelo carregado")

def getUserImages(user_id: str): 
  file = open(USERS_PATH + "/" + user_id + '.txt', 'r')  
  user_images = [img.strip() for img in file.readlines()]
  file.close()

  return user_images

def calcUserPreference(user_images: List[str]):
  num_of_categories = len(model.categories)
  user_preferences = np.full(num_of_categories, 0, dtype=float)

  for image in user_images:
    img_categories = model.predict(IMAGES_PATH + "/" + image) 
    user_preferences += img_categories
  
  user_preferences = np.divide(user_preferences, len(user_images))

  return user_preferences

def calcUsersDivergence(userA_prefs: List[float], userB_prefs: List[float]):
  num_of_categories = len(userA_prefs)

  Dkl_A_B = 0
  Dkl_B_A = 0

  for i in range(num_of_categories):
    Dkl_A_B += userA_prefs[i] * math.log(userA_prefs[i] / userB_prefs[i])
    Dkl_B_A += userB_prefs[i] * math.log(userB_prefs[i] / userA_prefs[i])

    Dkl = Dkl_A_B + Dkl_B_A

  return Dkl

def main() -> nx.Graph:
  users = os.listdir(USERS_PATH)
  users = list(sorted(users, key=lambda user: int(user.replace('.txt', ''))))

  users_preferences = {}

  for user in users:
    user_id = user.replace(".txt", "")
    user_images = getUserImages(user_id)

    users_preferences[user_id] = calcUserPreference(user_images)
    print("Preferências do usuário " + user_id)
  
  num_of_user = len(users_preferences)

  users_ids = np.array(list(users_preferences.keys()))

  users_divergences = np.empty((num_of_user, num_of_user), dtype=float)
  max_divergence = 0
  min_divergence = None
  for i in range(num_of_user):
    for j in range(i, num_of_user):
      if j == i:
        min_divergence = 0
        users_divergences[i][j] = 0
        users_divergences[j][i] = 0
        continue

      userA = users_preferences[users_ids[i]]
      userB = users_preferences[users_ids[j]]

      divergence = calcUsersDivergence(userA, userB)

      if divergence > max_divergence:
        max_divergence = divergence
      
      if min_divergence == None or divergence < min_divergence:
        min_divergence = divergence

      users_divergences[i][j] = divergence
      users_divergences[j][i] = divergence

      print(f"""[{users_ids[i]}, {users_ids[j]}]: {divergence:.4f}""")

  def normalize(value):
    return (1 - (value - min_divergence) / (max_divergence - min_divergence))

  normalizer = np.vectorize(normalize)

  users_divergences = normalizer(users_divergences)

  G = nx.Graph()
  for user_id in users_ids:
    G.add_node(user_id)

  for i in range(num_of_user):
    for j in range(num_of_user):
      if i == j:
        continue
      
      weight = users_divergences[i][j]
      if weight == 0:
        continue

      G.add_edge(users_ids[i], users_ids[j], weight=users_divergences[i][j])
      G.add_edge(users_ids[j], users_ids[i], weight=users_divergences[j][i])

  float_formatter = "{:.4f}".format
  np.set_printoptions(formatter={'float_kind':float_formatter})

  user_id_reference = {}
  for i, user_id in enumerate(users_ids): 
    user_id_reference[user_id] = i
  

  plt.figure(figsize=(6, 6))
  pos = nx.spring_layout(G, k=3)  
  nx.draw(G, pos, with_labels=True, node_color='#2C4C7C', edge_color='#3F5BD2', font_color="#FFFFFF", node_size=250, width=0.5)
  edge_labels = dict([((u,v,), f"{d['weight']:.2f}") for u,v,d in G.edges(data=True)])
  nx.draw_networkx_edge_labels(G, pos, edge_labels)
  plt.show()

  return G

main()



      
