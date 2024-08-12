from typing import List
import numpy as np
import math
import os

from Inception_V3 import Inception_V3

USERS_PATH = './users_created_data/'

model = Inception_V3()
print("Modelo carregado")

def getUserImages(user_id: str): 
  file = open(USERS_PATH + user_id + '.txt', 'r')  
  user_images = [img.strip() for img in file.readlines()]
  file.close()

  return user_images

def calcUserPreference(user_images: List[str]):
  num_of_categories = len(model.categories)
  user_preferences = np.full(num_of_categories, 0, dtype=float)

  for image in user_images:
    img_categories = model.predict(image) 
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

def test():
  users = os.listdir(USERS_PATH)

  users_preferences = {}

  for user in users:
    user_id = user.replace(".txt", "")
    user_images = getUserImages(user_id)

    users_preferences[user_id] = calcUserPreference(user_images)
    print("Preferências do usuário " + user_id)
  
  users_ids = np.array(list(users_preferences.keys()))
  for i in range(len(users_preferences)):
    for j in range(i + 1, len(users_preferences)):
      userA = users_preferences[users_ids[i]]
      userB = users_preferences[users_ids[j]]

      divergence = calcUsersDivergence(userA, userB)
      print(f"""[{users_ids[i]}, {users_ids[j]}]: {divergence:.4f}""")

test()



      
