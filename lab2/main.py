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

from typing import Dict, List, Tuple


def get_input_graph(filename: str, 
                    v1: List[str],
                    v2: List[str], 
                    e: List[Tuple[str]]):
    with open(filename, "r") as f:
        p1, p2 = [int(x) for x in f.readline().split()]
        v1 += f.readline().split()
        v2 += f.readline().split()
        for line in f.readlines():
            a,b = line.strip().split()
            e.append((a, b))

def check_if_bigrapsh():
    pass

def find_major_matching(v1: List[str], 
                        v2: List[str], 
                        e: List[Tuple[str]]):
    
    x: Dict[str, bool] = {}
    incd_v1: Dict[str, List[str]] = {}
    major_matching: Dict[str, str] = {}
    
    for v in v1:
        incd_v1[v] = []
        for u in v2:
            if((v, u) in e or (v, u) in e):
                incd_v1[v].append(u)

    for u in v2:
        major_matching[u] = 0
    
    for v in v1:
        for u in v1:
            x[u] = False
        augmental(v, x, incd_v1, major_matching)
        
    return major_matching


def augmental(v:str,
              marked_v1: Dict[str, bool], 
              incd_v1: Dict[str, List[str]], 
              matchings: Dict[str, str]):
    
    stack = [ (v, marked_v1, incd_v1, matchings) ]
    
    if(marked_v1[v]):
        return False
    marked_v1[v] = True
    for u in incd_v1[v]:
        if(matchings[u] == 0 or augmental(matchings[u], marked_v1, incd_v1, matchings)):
            matchings[u] = v
            return True
    return False


def write_major_matching(filename: str, mm: Dict[str, str]):
    out_fname = "matching_" + filename
    with open(out_fname, "w+") as f:
        for key in mm.keys():
            if(mm[key] != 0):
                f.write(f"{mm[key]} {key}\n")


def generate_complete_bigraph(filename:str, p1: int, p2: int):
    with open(filename, "w+") as f:
        f.write(f"{p1} {p2}\n")
        
        f.write(" ".join(["A" + str(i) for i in range(1,p1+1)]))
        f.write("\n")
        f.write(" ".join(["B" + str(i) for i in range(1,p2+1)]))
        f.write("\n")
        for i in range(1, p1+1):
            for j in range(1, p2+1):
                f.write(f"A{i} B{j}\n")
        

def main():
    v1 = []
    v2 = []
    e = []
    while(True):
        try:
            option = input("\n\nWrite chosen option (Ctrl+C to exit):\n 1 - process a file\n 2 - generate a file with complete bi-graph\n")
            
            filename = input("\nWrite file name (.txt):\n")
            
            match option:
                case "1":
                    get_input_graph(filename, v1, v2, e)
                    mm = find_major_matching(v1, v2, e)
                    write_major_matching(filename, mm)
                    print(f"Major matching is in {'matching_' + filename}")
                    v1.clear()
                    v2.clear()
                    e.clear()
                case "2":
                    p1 = int(input("Write amount of vertexes of first graph:  "))
                    p2 = int(input("Write amount of vertexes of second graph: "))
                    
                    generate_complete_bigraph(filename, p1, p2)
                    
                    print("Complete bi-graph generated")

        except KeyboardInterrupt:
            print("Program is terminated")
            break
    

if __name__ == '__main__':
    main()