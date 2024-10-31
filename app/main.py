from app.modulo1 import Modulo1
from app.modulo2 import Modulo2
from app.modulo3 import Modulo3
from app.modulo4 import Modulo4
from app.modulo5 import Modulo5
from app.modulo6 import Modulo6
from app.modulo7 import Modulo7

from app.utils.getArgs import getTestFiles
from app.utils.randomId import generateRandomId

from app.models.Case import Case
from app.models.Connection import Connection

class App:
    def __init__(self, test=None, print_data=False):
        self.print_data = print_data
        self.files = getTestFiles(test)

        self.current_state = Case()

        self.m1 = Modulo1(print_data)
        self.m2 = Modulo2(print_data)
        self.m3 = Modulo3(self.files.get("police-database"), print_data)
        self.m4 = Modulo4(print_data)
        self.m5 = Modulo5(print_data)
        self.m6 = Modulo6(print_data)
        self.m7 = Modulo7(print_data)

    def execute(self, return_rank=False):
        if not self.files:
            persons = self.m2.main()
            self.m3.main([p.document for p in persons])
            self.m1.main()
            self.m4.main()
            self.m5.main()
            self.m6.main()

            rank = self.m7.main(return_rank=return_rank)

            if rank:
                return rank
            return None

        for i, step in enumerate(self.files.get("steps")):
            m2_files = {
                "pessoas": step.get("pessoas"),
                "conexoes": step.get("conexoes"),
                "vitimas": self.files.get("vitimas") if i == 0 else None,
            }

            persons = self.m2.main(m2_files)
            self.m3.main([p.document for p in persons])
            self.m1.main(step["users_images"])
            facts_values_file = step.get("fatos")
            self.m4.main(facts_values_file)

        self.m5.main()
        self.m6.main()
        rank = self.m7.main(return_rank=return_rank)
        if rank:
            return rank

    def add_connections_to_test(self, up_ids):
        conn_weight = 1
        conn_desc = "Ruído"

        conns: list[Connection] = []
        for i, conn in enumerate(up_ids):
            conn_id = len(self.current_state.connections) + i + 1
            id_p_a = conn[0]
            id_p_b = conn[1]
            graph_id = generateRandomId()
            new_conn = Connection(conn_id, id_p_a, id_p_b, conn_desc, conn_weight, graph_id)
            conns.append(new_conn)

        updated_persons, new_conns = self.m5.test(self.current_state, conns)
        updated_persons = self.m6.test(updated_persons, new_conns)
        # rank = self.m7.test(updated_persons)


        return []