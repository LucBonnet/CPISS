from matplotlib import pyplot as plt
import numpy as np
import math

from app.main import App
from app.models.Connection import Connection
from app.models.Graph import Graph
from app.models.UP import UP

def calc_auc(current_rank, expected_rank):
    x = []
    y = []
    for i, p in enumerate(current_rank):
        rank_pos = i + 1

        if p.document not in expected_rank:
            continue

        expected_pos = expected_rank.index(p.document) + 1

        deviation = math.fabs(expected_pos - rank_pos)

        score = 1 - (deviation / (len(current_rank) - 1))

        curr_x = (expected_pos - 1) / (len(expected_rank) - 1)
        x.append(curr_x)
        y.append(score)

    x.sort()

    i = np.trapz(y, x)
    return i


def create_matrix(id_persons):
    connections = Connection.getAll()

    conns = np.empty((len(id_persons), len(id_persons)), dtype=int)
    conns.fill(0)
    for c in connections:
        pa = c.id_person_a
        pb = c.id_person_b

        pa_index = id_persons.index(pa)
        pb_index = id_persons.index(pb)

        conns[pa_index][pb_index] = 1
        conns[pb_index][pa_index] = 1

    return conns


def main():
    expected_rank = ['456573409', '419976309', '288410774']

    app = App("FeraDaPenha")
    rank = app.execute(return_rank=True)

    area = calc_auc(rank, expected_rank)
    print("Área inicial:", area)

    persons = UP.getAll()
    id_persons = [p.up_id for p in persons]

    conns = create_matrix(id_persons)

    lista = []
    for i in range(len(conns)):
        for j in range(i, len(conns)):
            if i == j:
                continue

            if not conns[i][j]:
                lista.append([id_persons[i], id_persons[j]])

    # lista = lista[:10]
    print(lista)

    areas = []

    for k in range(1,len(lista) + 1):
        for i in range(0, len(lista)):
            conns = []
            for j in range(i, i+k):
                if i+k > len(lista):
                    continue
                print(lista[j], end="")
                ps = lista[j]
                graph = Graph.create(2)
                new_conns = Connection.create((ps[0], ps[1], "Ruído", 1, graph))
                conns = conns + new_conns

            if len(conns) == 0:
                continue

            rank = app.execute(return_rank=True)
            file = open("./rank.txt", "w", encoding="utf-8")
            for rank_p in rank:
                file.write(f"{rank_p.name} - {rank_p.importance}\n")
            file.close()
            area = calc_auc(rank, expected_rank)
            areas.append(area)
            print(area)
            
            Connection.delete_ruido()
            for p in persons:
                p.update_pl(p.participation_level)

            print()

    print(areas)
    avg = sum(areas) / len(areas)
    print(f"\nMédia:\n{avg:.10f}")

if __name__ == "__main__":
    main()
