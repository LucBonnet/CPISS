import os

# from app.modulo1 import Modulo1
from app.modulo2 import Modulo2
from app.modulo3 import Modulo3
from app.modulo4 import Modulo4
from app.modulo5 import Modulo5
from app.modulo6 import Modulo6
from app.modulo7 import Modulo7

from app.database.create_database import create as create_database
from Imagens_usuarios.createDataset import sample

from app.utils.getArgs import getArgs

def main():
    args = getArgs()
    test_files = args.get("files")
    reset_database = args.get("reset")

    create_database(reset_database)

    m2 = Modulo2()
    modulo2InitialData = {
        "pessoas": test_files.get("pessoas") if test_files else None,
        "conexoes": test_files.get("conexoes") if test_files else None,
        "vitimas": test_files.get("vitimas")if test_files else None,
    }
    persons = m2.main(modulo2InitialData)

    # m1 = Modulo1()
    # m1.main(ids)

    identifiers = list(map(lambda person: person[1], persons))
    
    police_database_file = test_files.get("police-database")
    m3 = Modulo3(police_database_file)
    m3.main(identifiers)

    facts_values_file = test_files.get("fatos")
    m4 = Modulo4()
    m4.main(facts_values_file)

    m5 = Modulo5()
    m5.main()

    m6 = Modulo6()
    m6.main()

    m7 = Modulo7()
    m7.main()
    
if __name__ == "__main__":
    main()