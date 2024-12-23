import matplotlib.pyplot as plt
import networkx as nx
from typing import List
import queue
import math

from app.utils.formatImportance import formatImportance

from app.database.database import db
from app.models.UP import UP
from app.models.Connection import Connection
from app.models.Victim import Victim

from app.modulo7.api import App

class Modulo7:
    def __init__(self, print_data=True):
        self.print_data = print_data
        self.graph = nx.Graph()
        self.Wi = 0.5
        self.Wc = 0.5
        self.order = -1

        self.persons = UP.getOrderByImportance()
        self.connections = Connection.getAll()
        self.victim = 0

    def func_edge_color(self, u, v, path):
        edge = [u, v]
        if edge in path:
            return "#FF0000"

        edge = [v, u]
        if edge in path:
            return "#FF0000"

        return "#3F5BD2"

    def calculaCaminho(self, id_pessoa, importancia):
        pq = queue.PriorityQueue()

        # Coloca a primeira pessoa na fila de prioridade
        pq.put((self.order * importancia, (id_pessoa, importancia * self.Wi, 0, [])))
        #      (-importancia, (id_pessoa, custo_acumulado = 0, caminho esta vazio pois é o primeiro caso))

        # Dicionário para armazenar o melhor caminho
        visitados = {}

        ups = set()
        path = []
        path1 = []
        while not pq.empty():
            _, pessoa_atual = pq.get()  # Remove e retorna o item de maior prioridade da fila de prioridade

            # Retorna uma tupla de dois valores(1: importancia, 2: pessoa atual(id_pessoa, custo_acumulado, caminho))
            id_pessoa_atual, custo_acumulado, num_pessoas, caminho = pessoa_atual  # Transforma o 2 valor da tupla na pessoa atual
            ups.add(id_pessoa_atual)

            # Se encontrou a vítima, imprime o caminho e encerra
            if id_pessoa_atual == self.victim:
                caminho.append(id_pessoa_atual)
                if self.print_data:
                    print(f"custo para encontrar a vitima: {custo_acumulado}")
                    print(f"caminho: {caminho}")
                path1=caminho
                for i in range(len(caminho)):
                    if i + 1 < len(caminho):
                        path.append([caminho[i], caminho[i + 1]])
                break

            # Se já foi visitada com um custo menor, pula essa pessoa
            if id_pessoa_atual in visitados and visitados[id_pessoa_atual] >= custo_acumulado:
                continue

            # Atualiza o caminho para incluir a pessoa atual
            caminho_atualizado = caminho + [id_pessoa_atual]

            # Marca como visitado com o menor custo
            visitados[id_pessoa_atual] = custo_acumulado

            # Consulta as conexões da pessoa atual
            sql = """
                SELECT 
                c."id_pessoa_A", 
                c."id_pessoa_B", 
                c.peso, 
                p1.importancia as imp_p_a, 
                p2.importancia as imp_p_b 
                FROM conexoes_finais as c 
                INNER JOIN pessoas as p1 
                on c."id_pessoa_A" = p1.id 
                INNER JOIN pessoas as p2 
                on c."id_pessoa_B" = p2.id
                WHERE c."id_pessoa_A" = ? OR c."id_pessoa_B" = ?
            """

            db.connect()
            conexoes = db.execute(sql, (id_pessoa_atual, id_pessoa_atual))
            db.close()

            for (id_p_a, id_p_b, peso, imp_p_a, imp_p_b) in conexoes:
                # Definir qual pessoa é o filho
                imp_filho = imp_p_a
                id_filho = id_p_a
                if id_pessoa_atual == id_p_a:
                    imp_filho = imp_p_b
                    id_filho = id_p_b

                # Calcula novo valor acumulado para o filho com base nos pesos das conexões
                # valor = (imp_filho * self.Wi) + (peso * self.Wc)
                # valor_acumulado = custo_acumulado + valor - num_pessoas

                heuristica = (imp_filho * self.Wi) + (peso * self.Wc) + custo_acumulado
                custo = num_pessoas
                valor = heuristica + custo

                if id_filho not in ups:
                    # Coloca na fila de prioridade (-valor_acumulado para priorizar maior peso)
                    
                    # pq.put((self.order * valor_acumulado, (id_filho, valor_acumulado, num_pessoas + 1, caminho_atualizado)))
                    pq.put((valor, (id_filho, heuristica, num_pessoas + 1, caminho_atualizado)))
                    
        return path1

    def get_path(self, person_id):
        if not person_id:
            return None
        
        person = None
        for p in self.persons:
            if str(p.up_id) == person_id:
                person = p
                break

        if person is None:
            return None
        
        path = self.calculaCaminho(person.up_id, person.importance)
        return path

    def draw_graph(self, path: List[List[str]]):
        persons = UP.getAll()

        labels = {}
        for person in persons:
            self.graph.add_node(person.up_id)
            labels[person.up_id] = f"{person.name}\n{formatImportance(person.importance)}%"

        connections = Connection.getAll()

        for connection in connections:
            self.graph.add_edge(connection.id_person_a, connection.id_person_b, weight=connection.weight)

        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(self.graph)
        edge_color = [self.func_edge_color(u, v, path) for u, v in self.graph.edges]
        nx.draw(self.graph, pos, with_labels=False, node_color='#2C4C7C', edge_color=edge_color, font_color="#FFFFFF",
                node_size=2000, width=0.5)
        edge_labels = dict([((u, v,), f"{d['weight']:.2f}") for u, v, d in self.graph.edges(data=True)])
        nx.draw_networkx_labels(self.graph, pos, labels, font_color="#FFFFFF", font_size=10)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)
        plt.show()

    def get_persons(self):
        persons = UP.getOrderByImportance()
        persons = list(map(lambda p: p.toJSON(), persons))
        return persons
    
    def get_victims(self):
        victims = Victim.getAll()
        victims = list(map(lambda v: v.toJSON(), victims))
        return victims

    def get_connections(self):
        connections = Connection.getAll()
        connections = list(map(lambda c: c.toJSON(), connections))
        return connections

    def get_graph(self):
        graph = nx.Graph()
        for person in self.persons:
            graph.add_node(person.up_id)

        self.connections = Connection.getAll()

        for connection in self.connections:
            graph.add_edge(connection.id_person_a, connection.id_person_b)

        k = len(self.persons) / 2 / math.sqrt(len(self.persons))
        iterations = round(3 / 4 * len(self.persons)) * 10
        if self.print_data:
            print("k = " + str(k))
            print("iterations = " + str(iterations))

        pos = nx.spring_layout(graph, scale=1, seed=self.connections[0].id_graph % 1000)

        persons = []
        for p in self.persons:
            json_p = p.toJSON() 
            person_pos = pos.get(p.up_id)
            json_p["position"] = {}
            json_p["position"]["x"] = person_pos[0]
            json_p["position"]["y"] = person_pos[1]
            persons.append(json_p)

        return persons

    def print_rank(self, rank):
        max_name_size = max([len(p.name) for p in rank])
        rank_facts_size = max([len("; ".join([str(f) for f in p.facts])) for p in rank])

        print("\nRanqueamento das unidades participantes:\n")

        header = ("POSIÇÃO", "ID", "NOME", "NP", "FATOS", "IMPORTÂNCIA")
        col_widths = (7, 4, max(max_name_size, 4), 6, max(rank_facts_size, 5), 12)
        def center(value, width):
            return str(value).center(width)
        
        print(" | ".join([center(header[i], col_widths[i]) for i in range(len(header))]))
        print("-+-".join(["-" * col_widths[i] for i in range(len(header))]))

        for i, person in enumerate(rank):
            facts = "; ".join([str(f) for f in person.facts])

            pos = f"{i+1}."
            importance = f"{round(person.importance * 100, 8)}%"
            print(" | ".join([
                f"{pos:>{col_widths[0]}}", 
                f"{center(person.up_id, col_widths[1])}",  
                f"{person.name:<{col_widths[2]}}",
                f"{center(person.participation_level, col_widths[3])}",
                f"{center(facts,col_widths[4])}",
                f"{center(importance, col_widths[5])}",
            ]))
        print()

    def main(self, return_rank=False):
        print("Módulo 7")
        
        id_vitima = 0
        victims = Victim.getAll()

        if len(victims) == 0:
            print("Vítima não encontrada")
            return

        victim = victims[0]
        id_vitima = victim.person_id

        victim = UP.findById(id_vitima)

        if self.print_data:
            persons = UP.getAll()
            for person in persons:
                print()
                print(person)
                print()

        if self.print_data:
            print("\nVítima:")
            print(victim)
        self.victim = victim.up_id

        self.persons = UP.getOrderByImportance()

        rank: list[UP] = []
        for i, up in enumerate(self.persons):
            rank.append(up)

        if self.print_data:
            for p in rank:
                path = self.calculaCaminho(p.up_id, p.importance)
                print(path)

        self.print_rank(rank)

        if return_rank:
            return rank

        App(self)

    def get_rank(self, persons: list[UP]):
        persons = list(sorted(persons, key=lambda p: p.importance, reverse=True))
        return persons