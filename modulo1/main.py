from typing import List
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

def main() -> List[List[float]]:
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

      # print(f"""[{users_ids[i]}, {users_ids[j]}]: {divergence:.4f}""")

  def normalize(value):
    return (1 - (value - min_divergence) / (max_divergence - min_divergence))

  normalizer = np.vectorize(normalize)

  users_divergences = normalizer(users_divergences)

  float_formatter = "{:.4f}".format
  np.set_printoptions(formatter={'float_kind':float_formatter})
  print(users_divergences)

  return users_divergences

main()



      
