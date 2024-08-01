import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math
import os

from Inception_V3 import Inception_V3

PLOT_DATA = True

model = Inception_V3()
print("Modelo carregado")

def plotData(user_id, preferences):
  plt.plot(preferences)
  plt.title("Usuário " + str(user_id))
  plt.show()
  print(model.topCategories(preferences, 10))

def getUsersImages():
  users_images = {}

  users = os.listdir('./users_created_data')

  for user in users:
    with open('./users_created_data/' + user, 'r') as file:
      user_images = [img.strip() for img in file.readlines()]
      users_images[user.replace('.txt', '')] = user_images

  return users_images    

def getImageClasses(img_path):
  result = model.predict(img_path)
  return result

def getUserPreference(images):
  user_preference = []
  for i in range(len(model.categories)):
    value = 0
    for j in range(len(images)):
      value += images[j][i]
    user_preference.append(value / len(images))
  
  return user_preference

def getUsersDivergence(userA, userB):
  Dkl_A_B = 0
  for i in range(len(userA)):
    Dkl_A_B += userA[i] * math.log(userA[i] / userB[i])
  
  Dkl_B_A = 0
  for i in range(len(userB)):
    Dkl_B_A += userB[i] * math.log(userB[i] / userA[i])
  
  Dkl = Dkl_A_B + Dkl_B_A

  return Dkl  

def main():
  users_images = getUsersImages()

  users_prefs = {}
  for user_id, user_images in users_images.items():
    images = []
    for image in user_images:
      img_classification = getImageClasses(image)
      images.append(img_classification)
    
    users_prefs[user_id] = getUserPreference(images)

  users_ids = np.array(list(users_prefs.keys()))
  for i in range(users_ids.size):
    for j in range(i + 1, users_ids.size):
      userA = users_prefs[users_ids[i]]
      userB = users_prefs[users_ids[j]]
      divergence = getUsersDivergence(userA, userB)

      print(f"""[{users_ids[i]}, {users_ids[j]}]: {divergence:.4f}""")

main() 

