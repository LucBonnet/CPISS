import random
import os

IMAGE_NAME_PREFIX = 'image'
IMAGE_FILE_EXTENSION = '.jpg'

USERS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'users_data')

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

def clearData():
  users_files = os.listdir(USERS_PATH)
  for file in users_files:
    os.remove(USERS_PATH + "/" + file)

users = {}

def createData(ids):
  num_of_users = len(ids)
  for i in range(num_of_users):  
    user_id = str(ids[i])

    file_name = user_id + '.txt'
    file = open(USERS_PATH + "/" + file_name, 'w')

    category_index = random.randint(0, len(categories) - 1)
    users[user_id] = category_index
    category = categories[category_index]
    tam_category = category[1] - category[0] + 1
    num_of_images = random.randint(10, tam_category)

    for j in range(num_of_images):
      image_num = random.randint(category[0], category[1])
      img_full_path = IMAGE_NAME_PREFIX + str(image_num) + IMAGE_FILE_EXTENSION
      file.write(img_full_path + '\n')

    file.close()
    

def main(ids): 
  clearData()

  createData(ids)
  for user_id, category_id in users.items():
    print(f"""{user_id} => {category_id}""")

def sample():
  num_of_users = 50
  ids = list(range(1, num_of_users + 1))

  main(ids)