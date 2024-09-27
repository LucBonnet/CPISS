import os
from app.utils.argsParser import argsParser

def getArgs():
  args = argsParser()

  result = {
    "files": None,
    "reset": False,
  }
  if args.get("t"):
    path_name = args.get("t")

    files = getTestFiles(path_name)
    if files:
      result["files"] = files

  if args.get("r"):
    result["reset"] = True

  return result

def getTestFiles(path_name: str) -> None | dict:
  tests_dir = os.path.join(os.path.dirname(__file__), '..', '..', "tests")
  test_path = os.path.join(tests_dir, path_name)
  
  if not os.path.exists(test_path):
    print(f'Caso de teste "{path_name}" não encontrado')
    return None

  initialData = {}
  
  files = ["conexoes.txt", "fatos.txt", "pessoas.txt", "vitimas.txt", "police-database.json"]
  for file in files:
    file_path = os.path.join(test_path, file)
    if os.path.exists(file_path):
      file_name = file.split(".")[0]
      initialData[file_name] = os.path.realpath(file_path)
    else:
      print(f'Arquivo {file} não encontrado')  
    
  return initialData
