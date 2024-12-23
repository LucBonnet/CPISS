import os

from app.models.UP import UP
from app.models.Graph import Graph
from app.models.Connection import Connection
from app.models.Victim import Victim

persons_file_path = os.path.join(os.path.dirname(__file__), "pessoas.txt")
connections_file_path = os.path.join(os.path.dirname(__file__), "conexoes.txt")
victims_file_path = os.path.join(os.path.dirname(__file__), "vitimas.txt")


class Modulo2:
    def __init__(self, print_data=True) -> None:
        self.print_data = print_data
        
    def getDataFromFiles(self, files):
        if not files:
            return [], [], []

        persons_file_path = files.get("pessoas")
        connections_file_path = files.get("conexoes")
        victims_file_path = files.get("vitimas")

        persons = []
        if persons_file_path:
            with open(persons_file_path, 'r', encoding="utf-8") as persons_file:
                for person in persons_file.readlines():
                    name, identifier = person.split(";")
                    persons.append((name.strip(), identifier.strip()))

        connections = []
        if connections_file_path:
            with open(connections_file_path, 'r', encoding="utf-8") as connections_file:
                for conn in connections_file.readlines():
                    id_p_a, id_p_b, description = conn.split(";")
                    connections.append((id_p_a.strip(), id_p_b.strip(), description.strip()))

        victims = []
        if victims_file_path:
            with open(victims_file_path, 'r', encoding="utf-8") as victims_file:
                for victim in victims_file.readlines():
                    victims.append(victim.strip())

        return persons, connections, victims

    def main(self, modulo2_initial_data=None):
        print("\nMódulo 2")
        pessoas_arquivo, conexoes_arquivo, vitimas_arquivo = self.getDataFromFiles(modulo2_initial_data)

        created_persons = UP.create(pessoas_arquivo)
        num_persons = len(created_persons)
        print(f"Unidades participantes cadastradas: {num_persons} \n")

        if len(created_persons) == 0:
            return []

        print("Conexões:")
        for conn in conexoes_arquivo:
            code_person_a, code_person_b, description = conn

            person_a = UP.findByCode(code_person_a)
            if not person_a:
                raise Exception(f"Erro ao criar conexão\nPessoa {code_person_a} não encontrada")

            person_b = UP.findByCode(code_person_b)
            if not person_b:
                raise Exception(f"Erro ao criar conexão\nPessoa {code_person_b} não encontrada")

            graph_id = Graph.create(2)

            Connection.create((person_a.up_id, person_b.up_id, description, 1, graph_id))
            print(f"Adicionada conexão {person_a.name} - {person_b.name}")
        
        print()

        if len(vitimas_arquivo) > 0:
            print("Vítimas cadastradas:")

            for victim in vitimas_arquivo:
                up_victim = UP.findByCode(victim)
                Victim.create(up_victim.up_id)
                print(f"{up_victim.name}")
            print()
        

        return created_persons
