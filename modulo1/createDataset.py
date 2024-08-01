import random
import time
import os

top_view = (1, 30)
airplane = (31, 123)
elephant = (124, 219)
arrow = (220, 263)
lion = (264, 366)
bear = (367, 433)
polar_bear = (434, 470)
person = (471, 509)
sunset = (510, 611)
texture = (612, 786)
car = (787, 961)

categories = [top_view, airplane, elephant, arrow, lion, bear, polar_bear, person, sunset, texture, car]

num_of_users = 10

def clearData():
  users_files = os.listdir('./users_created_data/')
  for file in users_files:
    os.remove('./users_created_data/' + file)

def generateUserId():
  rnd_code = random.randint(1000, 9999)
  timestamp = round(time.time() * 1000000)
  return str(timestamp) + str(rnd_code)

users = {}

def createData():
  for i in range(num_of_users):  
    user_id = str(i+1)

    file_name = user_id + '.txt'
    file = open('./users_created_data/' + file_name, 'w')

    category_index = random.randint(0, len(categories) - 1)
    users[user_id] = category_index
    category = categories[category_index]
    tam_category = category[1] - category[0] + 1
    num_of_images = random.randint(10, tam_category)
    for j in range(num_of_images):
      image_num = random.randint(category[0], category[1])
      file.write('./Generalist961/image' + str(image_num) + '.jpg\n')

    file.close()
    

def main(): 
  clearData()

  createData()
  for user_id, category_id in users.items():
    print(f"""{user_id} => {category_id}""")

main()