from matplotlib import pyplot as plt
import numpy as np
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

        score = 1 - (deviation / (len(rank) - 1))

        curr_x = (expected_pos - 1) / (len(expected_rank) - 1)
        x.append(curr_x)
        y.append(score)

        score *= 100
        print(f"{p.name}: {score:.4f}%")

    x.sort()

    i = np.trapezoid(y, x) * 100
    print(f"Área: {i:.4f}%")

    plt.plot(x, y)
    plt.axis((0, 1, 0, 1))
    plt.show()


if __name__ == "__main__":
    main()
