import matplotlib.pyplot as plt
import networkx as nx

import queue

from app.utils.formatImportance import formatImportance

from app.database.database import db
from app.models.UP import UP
from app.models.Connection import Connection
from app.models.Victim import Victim


class Modulo7:
    def __init__(self):
        self.graph = nx.Graph()
        self.Wi = 0.5
        self.Wc = 0.5
        self.order = -1

    def func_edge_color(self, u, v, path):
        edge = [u, v]
        if edge in path:
            return "#FF0000"

        edge = [v, u]
        if edge in path:
            return "#FF0000"

        return "#3F5BD2"

    def calculaCaminho(self, id_vitima, id_pessoa, importancia):
        pq = queue.PriorityQueue()

        # Coloca a primeira pessoa na fila de prioridade
        pq.put((self.order * importancia, (id_pessoa, importancia * self.Wi, 0, [])))
        #      (-importancia, (id_pessoa, custo_acumulado = 0, caminho esta vazio pois é o primeiro caso))

        # Dicionário para armazenar o melhor caminho
        visitados = {}

        ups = set()
        path = []
        while not pq.empty():
            _, pessoa_atual = pq.get()  # Remove e retorna o item de maior prioridade da fila de prioridade

            # Retorna uma tupla de dois valores(1: importancia, 2: pessoa atual(id_pessoa, custo_acumulado, caminho))
            id_pessoa_atual, custo_acumulado, num_pessoas, caminho = pessoa_atual  # Transforma o 2 valor da tupla na pessoa atual
            ups.add(id_pessoa_atual)

            # Se encontrou a vítima, imprime o caminho e encerra
            if id_pessoa_atual == id_vitima:
                caminho.append(id_pessoa_atual)
                print(f"custo para encontrar a vitima: {custo_acumulado}")
                print(f"caminho: {caminho}")
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
                c.id as id_conexao,
                c."id_pessoa_A", 
                c."id_pessoa_B", 
                c.peso, 
                p1.importancia as imp_p_a, 
                p2.importancia as imp_p_b 
                FROM conexoes as c 
                INNER JOIN pessoas as p1 
                on c."id_pessoa_A" = p1.id 
                INNER JOIN pessoas as p2 
                on c."id_pessoa_B" = p2.id
                WHERE c."id_pessoa_A" = ? OR c."id_pessoa_B" = ?
            """

            db.connect()
            conexoes = db.execute(sql, (id_pessoa_atual, id_pessoa_atual))
            db.close()

            for (id_conexao, id_p_a, id_p_b, peso, imp_p_a, imp_p_b) in conexoes:
                # Definir qual pessoa é o filho
                imp_filho = imp_p_a
                id_filho = id_p_a
                if id_pessoa_atual == id_p_a:
                    imp_filho = imp_p_b
                    id_filho = id_p_b

                # Calcula novo valor acumulado para o filho com base nos pesos das conexões
                valor = (imp_filho * self.Wi) + (peso * self.Wc)
                valor_acumulado = custo_acumulado + valor - num_pessoas

                if id_filho not in ups:
                    # Coloca na fila de prioridade (-valor_acumulado para priorizar maior peso)
                    pq.put((self.order * valor_acumulado, (id_filho, valor_acumulado, num_pessoas + 1, caminho_atualizado)))

        return path

    def draw_graph(self, path: list[list[str]]):
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

    def main(self):
        print("Módulo 7")

        id_vitima = 0
        victims = Victim.getAll()

        if len(victims) == 0:
            print("Vítima não encontrada")
            return

        victim = victims[0]
        id_vitima = victim.person_id

        up_victim = UP.findById(id_vitima)

        persons = UP.getAll()
        for person in persons:
            print()
            print(person)
            print()

        print("\nVítima:")
        print(up_victim)

        # Primeira pessoa   (Mudar o numero do limit para mudar a quantidade de ids que quer na lista de maior importancia)
        ups = UP.getOrderByImportance()

        if len(ups) == 0:
            return

        print("\nRanqueamento das unidades participantes:")
        for i, up in enumerate(ups):
            print(f"{(i + 1)}. {up.up_id} - {up.name} - {formatImportance(up.importance)}%")

        # escolher qual id vc quer na lista
        pessoa_maior_importancia = ups[0]

        path = self.calculaCaminho(id_vitima, pessoa_maior_importancia.up_id, pessoa_maior_importancia.importance)

        self.draw_graph(path)
