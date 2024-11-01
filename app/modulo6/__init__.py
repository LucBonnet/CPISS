from app.database.database import db
from app.models.UP import UP
from app.models.Connection import Connection


class Modulo6:
    def __init__(self, print_data=True):
        self.print_data = print_data
        self.omega = 0

    def get_nodes_degrees(self, connections: list[Connection]):
        degrees = {}

        for conn in connections:
            if degrees.get(conn.id_person_a) is None:
                degrees[conn.id_person_a] = 1
            else:
                degrees[conn.id_person_a] += 1

            if degrees.get(conn.id_person_b) is None:
                degrees[conn.id_person_b] = 1
            else:
                degrees[conn.id_person_b] += 1

        return degrees

    def __calc_np(self, np_value, max_np):
        return np_value / max_np

    def __calc_omega(self, degrees):
        degrees_sum = sum(degrees)
        max_degree = max(degrees)

        avg_degrees = degrees_sum / len(degrees)
        return 1 - (avg_degrees / (max_degree * 1.1))

    def __set_omega(self, connections: list[Connection]):
        degrees = self.get_nodes_degrees(connections)
        values = list(degrees.values())

        if len(values) > 0:
            self.omega = self.__calc_omega(values)
            if self.print_data:
                print(f"w = {self.omega}")
        return self.omega

    def __update_np(self, ups_ids, ups_np, max_np):
        sql = "UPDATE pessoas SET np_formatado = ? WHERE id = ?"

        db.connect()
        for i, up_id in enumerate(ups_ids):
            np_value = self.__calc_np(ups_np[i], max_np)
            db.insert(sql, (np_value, up_id))
        db.close()

    def __set_np(self):
        sql = "SELECT max(id) FROM pessoas"
        db.connect()
        result = db.execute(sql)
        db.close()
        max_id = result[0][0]

        np = 0
        if max_id is None:
            return np

        max_np = 0
        ups_ids = []
        ups_np = []
        batch_size = 100
        for i in range(0, max_id, batch_size):
            sql = "SELECT * FROM pessoas WHERE id >= ? AND id < ?"
            db.connect()
            result = db.execute(sql, (i, i + batch_size))
            db.close()

            for up in result:
                up_id = up[0]
                ups_ids.append(up_id)
                np = up[3]
                ups_np.append(np)

                if np > max_np:
                    max_np = np

        self.__update_np(ups_ids, ups_np, max_np)

    def __p(self, facts):
        value = 1
        for f in facts:
            if f is not None:
                value *= 1 - (f * self.omega)

        return 1 - value

    def main(self):
        print("Módulo 6")
        connections = Connection.getAll()
        self.__set_omega(connections)
        print("Omega calcluado")
        self.__set_np()
        print("Níveis de participação atualizados")

        sql = "SELECT id FROM pessoas ORDER BY id"
        db.connect()
        result = db.execute(sql)
        db.close()

        for up_id, in result:
            sql = "SELECT * FROM pessoa_fato WHERE id_pessoa = ?"

            db.connect()
            result = db.execute(sql, (up_id,))
            db.close()

            facts = []
            for person_fact in result:
                fact_id = person_fact[2]
                sql = "SELECT valor FROM fatos WHERE id = ?"
                db.connect()
                value = db.execute(sql, (fact_id,))[0][0]
                db.close()
                facts.append(value)

            sql = "SELECT * FROM pessoas WHERE id = ?"

            db.connect()
            result = db.execute(sql, (up_id,))
            db.close()

            if len(result) > 0:
                person = UP(*result[0])
                facts.append(person.formatted_pl)

            importance = self.__p(facts)

            sql = "UPDATE pessoas SET importancia = ? WHERE id = ?"

            db.connect()
            db.execute(sql, (importance, up_id))
            db.close()

        print("Atualização das importâncias")

    def test(self, persons: list[UP], connections):
        self.__set_omega(connections)
        pls = [p.participation_level for p in persons]
        max_pl = max(pls)

        for p in persons:
            p.formatted_pl = self.__calc_np(p.participation_level, max_pl)
            facts = p.facts + [p.formatted_pl]
            p.importance = self.__p(facts)
        
        return persons

        
                

        
