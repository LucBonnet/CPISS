import random as rdn
import time

def generateRandomId():
  random = rdn.randint(10000, 99999)
  timestamp = round(time.time() * 1000)
  return int(f"{timestamp}{random}")