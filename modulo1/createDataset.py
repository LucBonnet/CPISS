import random
import os

IMAGES_PATH = './Generalist961/'
IMAGE_NAME_PREFIX = 'image'
IMAGE_FILE_EXTENSION = '.jpg'

USERS_PATH = './users_created_data'

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
  users_files = os.listdir(USERS_PATH)
  for file in users_files:
    os.remove(USERS_PATH + file)

users = {}

def createData():
  for i in range(num_of_users):  
    user_id = str( i + 1)

    file_name = user_id + '.txt'
    file = open(USERS_PATH + file_name, 'w')

    category_index = random.randint(0, len(categories) - 1)
    users[user_id] = category_index
    category = categories[category_index]
    tam_category = category[1] - category[0] + 1
    num_of_images = random.randint(10, tam_category)

    for None in range(num_of_images):
      image_num = random.randint(category[0], category[1])
      img_full_path = IMAGES_PATH + IMAGE_NAME_PREFIX + str(image_num) + IMAGE_FILE_EXTENSION
      file.write(img_full_path + '\n')

    file.close()
    

def main(): 
  clearData()

  createData()
  for user_id, category_id in users.items():
    print(f"""{user_id} => {category_id}""")

main()