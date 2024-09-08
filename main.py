# from app.modulo1 import Modulo1
from app.modulo2 import Modulo2
from app.modulo3 import Modulo3
from app.modulo4 import Modulo4
from app.modulo5 import Modulo5
from app.modulo6 import Modulo6
from app.modulo7 import Modulo7

from app.database.create_database import create as create_database
from Imagens_usuarios.createDataset import sample

def main():
    create_database()

    m2 = Modulo2()
    ids, persons = m2.main()

    # m1 = Modulo1()
    # m1.main(ids)

    rgs = list(map(lambda person: person[1], persons))
    
    m3 = Modulo3()
    m3.main(rgs)

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