import matplotlib.pyplot as plt
from typing import List
import networkx as nx
import numpy as np
import math
import os

from app.database.database import db
from app.utils.randomId import generateRandomId
from app.modulo1.Inception_V3 import Inception_V3

IMAGES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'Imagens_usuarios', 'Generalist961')
USERS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'Imagens_usuarios', 'users_data')

class Modulo1:
  def __init__(self):
    self.model = Inception_V3()
    self.num_of_categories = len(self.model.categories)
    print("Modelo carregado")
    
    self.graph_id = generateRandomId()
    db.connect()
    sql = """INSERT INTO grafos (id, etapa) VALUES (?,?)"""
    db.insert(sql, (self.graph_id, 1))
    db.close()
  
  def getUserImages(self, user_id: str): 
    try: 
      with open(USERS_PATH + "/" + str(user_id) + '.txt', 'r') as file: 
        user_images = [img.strip() for img in file.readlines()]

      return user_images
    except:
      return []

  def calcUserPreference(self, user_images: List[str]):
    user_preferences = np.full(self.num_of_categories, 0, dtype=float)

    for image in user_images:
      img_categories = self.model.predict(IMAGES_PATH + "/" + image) 
      user_preferences += img_categories
    
    user_preferences = np.divide(user_preferences, len(user_images))

    return user_preferences

  def calcUsersDivergence(self, userA_prefs: list[float], userB_prefs: list[float]):
    Dkl_A_B = 0
    Dkl_B_A = 0

    for i in range(self.num_of_categories):
      Dkl_A_B += userA_prefs[i] * math.log(userA_prefs[i] / userB_prefs[i])
      Dkl_B_A += userB_prefs[i] * math.log(userB_prefs[i] / userA_prefs[i])

      Dkl = Dkl_A_B + Dkl_B_A

    return Dkl
  
  def setDivergence(self, user_a_id, user_b_id, divergence):
    db.connect()
    sql = f"INSERT OR REPLACE INTO conexoes (id_pessoa_A, id_pessoa_B, peso, id_grafo) VALUES (?,?,?,?)"
    db.insert(sql, (user_a_id, user_b_id, divergence, self.graph_id))
    db.close()


  def comparePreferences(self):
    db.connect()
    sql = f"SELECT * FROM preferencias"
    preferences = db.execute(sql)
    db.close()
    
    num_of_users = len(preferences)
    
    users_divergences = np.empty((num_of_users, num_of_users), dtype=float)
    users_ids = [pref[0] for pref in preferences]

    max_divergence = 0
    min_divergence = None
    for i in range(num_of_users):
      for j in range(i, num_of_users):
        if i == j:  
          min_divergence = 0
          continue

        values = preferences[i][1]
        userA_prefs = [float(value) for value in values.split(";")]

        values = preferences[j][1]
        userB_prefs = [float(value) for value in values.split(";")]

        divergence = self.calcUsersDivergence(userA_prefs, userB_prefs)

        if divergence > max_divergence:
          max_divergence = divergence

        if min_divergence == None or divergence < min_divergence:
          min_divergence = divergence

        users_divergences[i][j] = divergence
        users_divergences[j][i] = divergence

        print(f"""[{users_ids[i]}, {users_ids[j]}]: {divergence:.4f}""")

    def normalize(value):
      return 1 - ((value - min_divergence) / (max_divergence - min_divergence))

    normalizer = np.vectorize(normalize)

    users_divergences = normalizer(users_divergences)

    for i in range(num_of_users):
      for j in range(i, num_of_users):
        if i == j:
          continue

        normalized_divergence = users_divergences[i][j]
        self.setDivergence(users_ids[i], users_ids[j], normalized_divergence)
    
    return users_divergences
    
  def main(self, person_ids: list[str]):
    print("Módulo 1")
    users = person_ids
    users_preferences = {}

    for user in users:
      user_id = str(user)
      user_images = self.getUserImages(user_id)
      if len(user_images) == 0:
        continue

      preferences = self.calcUserPreference(user_images)
      users_preferences[user_id] = preferences

      formatted_values = ";".join([format(pref, "e") for pref in preferences])

      db.connect()
      sql = """INSERT INTO preferencias (id_pessoa, valores) VALUES (?,?)"""
      db.execute(sql, (int(user_id), formatted_values))
      db.close()
      
      print("Preferências do usuário " + user_id)

    if len(person_ids) <= 1:
      return [[]]

    return self.comparePreferences()
      
def test():
  m1 = Modulo1()

  G = m1.main()

