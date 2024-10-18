from matplotlib import pyplot as plt
import math

from app.main import App


def main():
    expected_rank = ['456573409', '419976309', '288410774']

    app = App("FeraDaPenha")
    rank = app.execute(return_rank=True)

    for p in rank:
        print(f"{p.document} - {p.name}")

    x = []
    y = []
    for i, p in enumerate(rank):
        rank_pos = i + 1

        if p.document not in expected_rank:
            continue

        expected_pos = expected_rank.index(p.document) + 1

        deviation = math.fabs(expected_pos - rank_pos)

        score = 1 - (deviation / len(rank))

        x.append(expected_pos)
        y.append(score)

    x.sort()

    avg_precision = sum(y) / len(y)
    print(avg_precision)

    plt.plot(x, y)
    plt.axis((1, len(expected_rank), 0, 1))
    plt.show()


if __name__ == "__main__":
    main()
