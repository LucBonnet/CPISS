import os
from app.utils.argsParser import args_parser


def getArgs():
    args = args_parser()

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


def getTestFiles(path_name: str) -> dict:
    tests_dir = os.path.join(os.path.dirname(__file__), '..', '..', "tests")
    test_path = os.path.join(tests_dir, path_name)

    if not os.path.exists(test_path):
        raise Exception(f'Caso de teste "{path_name}" não encontrado')

    test_step_path = os.path.join(test_path, "passos")

    step_files = ["conexoes.txt", "fatos.txt", "pessoas.txt", "vitimas.txt"]
    steps = sorted([x[0] for x in os.listdir(test_step_path)])

    initialData = {}

    steps_files = []
    for i, step in enumerate(steps):
        step_path = os.path.join(test_step_path, step)

        data = {}
        for file in step_files:
            file_path = os.path.join(step_path, file)
            if os.path.exists(file_path):
                file_name = file.split(".")[0]
                data[file_name] = os.path.realpath(file_path)
            else:
                print(f'Arquivo {file} não encontrado no passo {(i + 1)}')

        images_path = os.path.join(step_path, "imagens_usuarios")
        if os.path.exists(images_path):
            data['users_images'] = os.path.realpath(images_path)
        else:
            data['users_images'] = None

        steps_files.append(data)

    initialData["steps"] = steps_files

    fixed_files = ["police-database.json"]
    for file in fixed_files:
        file_path = os.path.join(test_path, file)
        if os.path.exists(file_path):
            file_name = file.split(".")[0]
            initialData[file_name] = os.path.realpath(file_path)
        else:
            print(f'Arquivo {file} não encontrado')

    return initialData
