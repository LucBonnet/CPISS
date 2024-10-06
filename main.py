from app.modulo1 import Modulo1
from app.modulo2 import Modulo2
from app.modulo3 import Modulo3
from app.modulo4 import Modulo4
from app.modulo5 import Modulo5
from app.modulo6 import Modulo6
from app.modulo7 import Modulo7

from app.database.create_database import create as create_database
from Imagens_usuarios.createDataset import sample

from app.utils.getArgs import getArgs


def execute_test(test_files):
    police_database_file = test_files.get("police-database")

    m1 = Modulo1()
    m2 = Modulo2()
    m3 = Modulo3(police_database_file)
    m4 = Modulo4()
    m5 = Modulo5()
    m6 = Modulo6()
    m7 = Modulo7()

    for i, step in enumerate(test_files.get("steps")):
        m2_files = {
            "pessoas": step.get("pessoas"),
            "conexoes": step.get("conexoes"),
            "vitimas": test_files.get("vitimas") if i == 0 else None,
        }

        persons = m2.main(m2_files)


        identifiers = []
        if len(persons) > 0:
            identifiers = list(map(lambda person: person.document, persons))
        m3.main(identifiers)

        m1.main()

        facts_values_file = step.get("fatos")
        m4.main(facts_values_file)

        m5.main()

        m6.main()

        m7.main()


def main():
    args = getArgs()
    test_files = args.get("files")
    
    reset_database = args.get("reset")
    create_database(reset_database)

    if test_files:
        execute_test(test_files)
        return

    m2 = Modulo2()
    persons = m2.main()

    identifiers = []
    if len(persons) > 0:
        identifiers = list(map(lambda person: person.document, persons))

    m3 = Modulo3()
    m3.main(identifiers)
    
    m1 = Modulo1()
    m1.main()

    m4 = Modulo4()
    m4.main()

    m5 = Modulo5()
    m5.main()

    m6 = Modulo6()
    m6.main()

    m7 = Modulo7()
    m7.main()


if __name__ == "__main__":
    main()
