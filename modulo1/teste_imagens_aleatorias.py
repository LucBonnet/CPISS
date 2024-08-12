from Inception_V3 import Inception_V3
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import math

PLOT_DATA = True

model = Inception_V3()
print("Modelo carregado")

img1_path = "./imgs/img4.jpg"
result = model.predict(img1_path)
print("Imagem classificada")

if PLOT_DATA:
  fig, axs = plt.subplots(1, 2)
  img = mpimg.imread(img1_path)
  axs[0].plot(result)
  axs[1].imshow(img)
  axs[1].axis("off")
  plt.show()

categories = model.topCategories(result, 5)
for category, value in categories:
  print(category + ":" , value)

users_imgs = []
users_path = os.listdir('users')
users_path = list(sorted(users_path))
for user_path in users_path:
  users_imgs.append([os.path.join('users', user_path, file) for file in os.listdir(os.path.join("users", user_path))])

print(users_imgs)

users_preferences = []
for user in users_imgs:
  user_preferences = []
  for img_path in user:
    result = model.predict(img_path)
    user_preferences.append(result)
  users_preferences.append(user_preferences)

mean_users_preferences = []
for user_preferences in users_preferences:
  mean_user_preferences = []
  for i in range(len(model.categories)):
    prob_sum = 0
    for j in range(len(user_preferences)):
      prob_sum += user_preferences[j][i]
    mean = prob_sum / len(user_preferences)
    mean_user_preferences.append(mean)
  mean_users_preferences.append(mean_user_preferences)

print((len(mean_users_preferences), len(mean_users_preferences[0])))

for user in mean_users_preferences:
  plt.plot(user)
  plt.title("Usuário " + str(i + 1))
  plt.show()
  print(model.topCategories(user, 10))

tam = len(mean_users_preferences)
for i in range(tam):
  for j in range(i+1, tam):
    userA = mean_users_preferences[i]
    userB = mean_users_preferences[j]

    Dkl = 0
    for k in range(len(userA)):
      Dkl += userA[k] * math.log(userA[k] / userB[k])
  
    print("[" + str(i + 1) + ", " + str(j + 1) + "]:", Dkl)

    if PLOT_DATA: 
      plt.plot(userA)
      plt.plot(userB)
      plt.show()