# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
import random
import sys
import time

# 8 (a)
# implement an algorithm that given a graph G, set of adopters S,
# and a threshold q performs BRD where the adopters S never change.


def contagion_brd(G, S, q):
    Y = []
    for node in G:
        if node not in S:
            Y.append(node)
    while len(Y) > 0:
        switches = []
        new_Y = []
        for node in Y:
            x = 0
            neighbors = G[node]
            for neighbor in neighbors:
                if neighbor in S:
                    x += 1
            if float(x) / len(neighbors) >= q:
                switches.append(node)
            else:
                new_Y.append(node)
        if len(switches) == 0:
            break
        Y = new_Y
        S.extend(switches)

    return len(S) == len(G), len(S)


def question_8b():
    # Generate Graph
    G = {}
    with open("facebook_combined.txt", "r") as fhand:
        for line in fhand.readlines():
            i, j = [int(x) for x in line.strip("\n").split(" ")]
            if i not in G:
                G[i] = []
            G[i].append(j)
            if j not in G:
                G[j] = []
            if i not in G[j]:
                G[j].append(i)

    # Conduct Experiments
    success = 0
    infect_average = 0
    for i in range(100):
        S = []
        while len(S) != 10:
            node = random.randint(0, len(G))
            if node not in S:
                S.append(node)
        isCascaded, infect = contagion_brd(G, S, 0.1)
        if isCascaded:
            success += 1
        infect_average += infect
        if (i + 1) % 5 == 0:
            print("{} / 100".format(i + 1))
    infect_average /= 100.0

    return success, infect_average


def question_8c():
    # Generate Graph
    G = {}
    with open("facebook_combined.txt", "r") as fhand:
        for line in fhand.readlines():
            i, j = [int(x) for x in line.strip("\n").split(" ")]
            if i not in G:
                G[i] = []
            G[i].append(j)
            if j not in G:
                G[j] = []
            if i not in G[j]:
                G[j].append(i)
    print("Graph successfully constructed!")

    # Conduct Experiments
    results = []
    k_max = 260  # exclusive
    qq_max = 55  # exclusive
    for k in range(10, k_max, 10):
        new_result = []
        start_time = time.time()
        for qq in range(5, qq_max, 5):
            q = qq / 100.0
            success, infect_average = 0, 0
            for i in range(10):
                S = []
                while len(S) != k:
                    node = random.randint(0, len(G))
                    if node not in S:
                        S.append(node)
                isCascaded, infect = contagion_brd(G, S, q)
                if isCascaded:
                    success += 1
                infect_average += infect
            infect_average /= 10.0
            new_result.append((success, infect_average))
        results.append(new_result)
        epoch_time = time.time() - start_time
        print("k = {0}   {1:<6.1f}".format(k, epoch_time))

    with open("8c_results.txt", "w") as fhand:
        fhand.write("{0:<5}".format(""))
        for qq in range(5, qq_max, 5):
            q = qq / 100.0
            fhand.write("{0:<14.2}".format(q))
        fhand.write("\n")
        k = 10
        for result in results:
            fhand.write("{0:<5}".format(k))
            for r in result:
                rr = "{0}, {1:<6.1f}".format(r[0], r[1])
                fhand.write("{0:<14}".format(rr))
            fhand.write("\n")
            k += 10


if __name__ == "__main__":
    question = sys.argv[1]

    if question == "8a":
        figure = sys.argv[2]
        q = float(sys.argv[3])
        G = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
        S = [0, 1]
        if figure == "b":
            G = {0: [1], 1: [2], 2: [0, 1], 3: [4],
                 4: [2, 3, 6], 5: [6], 6: [4, 5]}
            S = [0, 1, 2]
        print(contagion_brd(G, S, q))
    elif question == "8b":
        print(question_8b())
    elif question == "8c":
        question_8c()
