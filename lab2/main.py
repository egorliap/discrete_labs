import random
from typing import Dict, List, Tuple
## Входной файл, граф G(V1, V2, E)
# Первая строка - 2 числа (p1 и p2): количество 
#    вершин в первой "доле" (V1) двудольного графа и во второй (V2) соответственно
# Вторая строка - p1 названий вершин из V1, перечисленных через пробел
# Третья строка - p2 названий вершин из V2, перечисленных через пробел
# Четвертая и последующие строки - ребра в этом графе, пара наименований двух вершин через пробел
#    (причем, для любого (a,b) принадлежащего множеству ребер E: a принадлежит V1, b - V2)
#
## Выходной файл, наибольшее паросочетание G(V1, V2, E)
# Каждая строка файла - пара, принадлежащая S - наибольшему паросочетанию
#
# Название выходного файла - matching_<input_filename>.txt


def get_input_graph(filename: str, v1: List[str], v2: List[str], e: List[Tuple[str, str]]):
    with open(filename, "r") as f:
        p1, p2 = map(int, f.readline().split())
        v1 += f.readline().strip().split()
        v2 += f.readline().strip().split()
        for line in f:
            a, b = line.strip().split()
            e.append((a, b))


def find_major_matching(v1: List[str], v2: List[str], e: List[Tuple[str, str]]):
    incd_v1 = {v: [] for v in v1}
    for v, u in e:
        incd_v1[v].append(u)

    major_matching = {u: None for u in v2}
    matched_v1 = {v: None for v in v1}

    def augmental_iterative(v: str):
        stack = [v]  
        visited_v1 = {v: False for v in v1}  
        prev = {v: None}  
        
        while stack:
            node = stack.pop()

            if node in v1:
                if visited_v1[node]:
                    continue
                visited_v1[node] = True
            else:
                continue

            for u in incd_v1[node]:
                if major_matching[u] is None:
                    
                    while node:
                        
                        next_node = matched_v1[node]
                        matched_v1[node] = u
                        major_matching[u] = node
                        u = next_node
                        node = prev.get(node)
                    return True
                elif not visited_v1[major_matching[u]]:
                    prev[major_matching[u]] = node
                    stack.append(major_matching[u])
        return False

    for v in v1:
        print(major_matching) 
        
        augmental_iterative(v)
        print(major_matching) 
        

    return matched_v1, major_matching


def write_major_matching(filename: str, mm: Dict[str, str]):
    out_fname = "matching_" + filename
    with open(out_fname, "w") as f:
        for u, v in mm.items():
            if v is not None:
                f.write(f"{v} {u}\n")


def generate_complete_bigraph(filename: str, p1: int, p2: int):
    with open(filename, "w") as f:
        f.write(f"{p1} {p2}\n")
        f.write(" ".join([f"A{i}" for i in range(1, p1 + 1)]) + "\n")
        f.write(" ".join([f"B{i}" for i in range(1, p2 + 1)]) + "\n")
        for i in range(1, p1 + 1):
            for j in range(1, p2 + 1):
                f.write(f"A{i} B{j}\n")


def generate_random_bigraph(filename: str, p1: int, p2: int, n: int):
    with open(filename, "w") as f:
        f.write(f"{p1} {p2}\n")
        f.write(" ".join([f"A{i}" for i in range(1, p1 + 1)]) + "\n")
        f.write(" ".join([f"B{i}" for i in range(1, p2 + 1)]) + "\n")
        for _ in range(n):
            f.write(f"A{random.randint(1, p1)} B{random.randint(1, p2)}\n")


def main():
    v1 = []
    v2 = []
    e = []

    while True:
        try:
            option = input(("\n\nWrite chosen option (Ctrl+C to exit):\n"
                           " 1 - process a file\n"
                           " 2 - generate a file with complete bi-graph\n" 
                           " 3 - generate a file with random bi-graph\n"))
            
            filename = input("\nWrite file name (.txt):\n")
            
            match option:
                case "1":
                    get_input_graph(filename, v1, v2, e)
                    matched_v1, major_matching = find_major_matching(v1, v2, e)
                    write_major_matching(filename, major_matching)
                    print(f"Major matching is in {'matching_' + filename}")
                    v1.clear()
                    v2.clear()
                    e.clear()
                case "2":
                    p1 = int(input("Write amount of vertexes of first graph:  "))
                    p2 = int(input("Write amount of vertexes of second graph: "))
                    generate_complete_bigraph(filename, p1, p2)
                    print("Complete bi-graph generated")
                case "3":
                    p1 = int(input("Write amount of vertexes of first graph:  "))
                    p2 = int(input("Write amount of vertexes of second graph: "))
                    n = int(input("Write amount of edges: "))
                    generate_random_bigraph(filename, p1, p2, n)
                    print("Random bi-graph generated")

        except KeyboardInterrupt:
            print("Program is terminated")
            break

if __name__ == '__main__':
    main()
