from matplotlib import pyplot as plt
import random as rdn
import numpy as np
import math
import os

from app.main import App
from app.models.Connection import Connection

from app.database.create_database import create as create_database
from app.utils.argsParser import args_parser

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

def write_file_with_rank(rank, num_conns, total, step, total_steps):
    file = open("./rank.txt", "w", encoding="utf-8")
    file.write(f"Conexões novas => {num_conns} / {total}\n")
    file.write(f"Etapa => {step} / {total_steps}\n")
    for rank_p in rank:
        file.write(f"{rank_p.name} - {rank_p.importance}\n")
    file.close()

def add_connections(test, expected_rank):
    app = App(test)
    rank = app.execute(return_rank=True)

    area = calc_auc(rank, expected_rank)
    print("Área inicial:", area)

    app.current_state.get_state()
    id_persons = [p.up_id for p in app.current_state.persons]

    conns = create_matrix(id_persons)

    lista = []
    for i in range(len(conns)):
        for j in range(i, len(conns)):
            if i == j:
                continue

            if not conns[i][j]:
                lista.append([id_persons[i], id_persons[j]])

    areas = []
    
    y = []
    x = []

    times = 1000
    for i in range(1, len(lista) + 1):
        # i -> Define quantas conexões serão adicionadas
        values = []
        for j in range(times):
            # j ->  Define a combinação testada

            # Seleciona i elementos da "lista" sem repetição
            list_to_test = rdn.sample(lista, i)

            rank = app.add_connections_to_test(list_to_test)
            write_file_with_rank(rank, i, len(lista), j, times)

            file = open(f"./tests-analise/rank-{i}-{j}.txt", "w")
            for p in rank:
                file.write(f"{p.name} - {p.importance} - {p.participation_level}\n")
            file.close()

            area = calc_auc(rank, expected_rank)
            values.append(area)
            areas.append(area)
            print(i, "-", area)

        avg = sum(values) / len(values) 
        y.append(avg)
        x.append(i)

    print(areas)
    avg = sum(areas) / len(areas)
    print(f"\nMédia:\n{avg:.10f}")

    print(min(y))
    print(max(y))

    plt.figure()
    plt.bar(x, y)
    plt.axis([1, len(x) + 1, 0, 1])
    plt.show()

def remove_connections(test, expected_rank):
    app = App(test)
    rank = app.execute(return_rank=True)

    area = calc_auc(rank, expected_rank)
    print("Área inicial:", area)

    app.current_state.get_state()

    connections = app.current_state.connections
    
    areas = []
    
    y = []
    x = []

    times = 1000
    for i in range(1, len(connections) + 1):
        # i -> Define quantas conexões serão retiradas
        values = []
        for j in range(times):
            # j ->  Define a combinação testada

            # Seleciona i elementos da "lista" sem repetição
            list_to_test = rdn.sample(connections, i)

            rank = app.remove_connections_to_test(list_to_test)
            write_file_with_rank(rank, i, len(connections), j, times)

            file = open(f"./tests-analise/rank-{i}-{j}.txt", "w")
            for p in rank:
                file.write(f"{p.name} - {p.importance} - {p.participation_level}\n")
            file.close()

            area = calc_auc(rank, expected_rank)
            values.append(area)
            areas.append(area)
            print(f"{i}, {j}", "-", area)

        avg = sum(values) / len(values) 
        y.append(avg)
        x.append(i)

    print(areas)
    avg = sum(areas) / len(areas)
    print(f"\nMédia:\n{avg:.10f}")

    print(min(y))
    print(max(y))

    plt.figure()
    plt.bar(x, y)
    plt.axis([1, len(x) + 1, 0, 1])
    plt.show()

def main():
    case_name = "FeraDaPenha"

    args = args_parser()

    reset_database = args.get("r")
    create_database(reset_database)

    expected_rank = ['456573409', '419976309', '288410774']


    # add_connections(case_name, expected_rank)
    remove_connections(case_name, expected_rank)
    

    # 0.7464575283
    # 0.7463966522


if __name__ == "__main__":
    main()
