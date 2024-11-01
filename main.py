from app.main import App
from app.database.create_database import create as create_database
from Imagens_usuarios.createDataset import sample

from app.utils.argsParser import args_parser

def main():
    args = args_parser()

    reset_database = args.get("r")
    create_database(reset_database)

    app = App(args.get("t"))
    rank = app.execute(return_rank=False)
    print(rank)

if __name__ == "__main__":
    main()
