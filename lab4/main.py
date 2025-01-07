import json
import networkx as nx
import matplotlib.pyplot as plt

 
def get_grapgh_from_file(filename, graph: dict[int, list]):
    with open(filename, "r") as f:
        n = f.readline()  # noqa: F841
        vertexes = f.readline().split()
        edges = []
        e = f.readline()
        while e!="":
            edges.append(e.split())
            e = f.readline()
    for v in vertexes:
        graph[v] = []
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return vertexes

def coloring(graph):
    vertices = sorted(graph, key=lambda v: -len(graph[v]))
    color_assignment = {v: -1 for v in vertices}  
    c = 1

    while vertices:
        available_vertices = []
        print("Enter")
        for v in vertices[:]:
            print(f"Current Vertex |v| = |{v}| = {len(graph[v])}")
            
            if all(color_assignment[u] != c for u in graph[v]):
                color_assignment[v] = c
                available_vertices.append(v)
        for v in available_vertices:
            vertices.remove(v)
        c += 1

    return color_assignment

while True:
    try:
        filename = input("\nEnter filename (.txt) with graph data (^C to exit): ")
    except KeyboardInterrupt:
        print("Exited")
        break
    
    graph = {}
    try:
        get_grapgh_from_file(filename, graph)
    except FileNotFoundError:
        print("File not found")
        continue

    ca = coloring(graph)
    print("Color assignment:")
    print(json.dumps(ca, separators=("",":"), sort_keys=True, indent=2))
        
    chromatic_number = max(ca.values())
    print("Chromatic number:", chromatic_number)
    
    G = nx.Graph(graph)
    plt.figure(figsize=(8,6))
    nx.draw(G, pos = nx.spring_layout(G), ax = None, with_labels = True,font_size = 20, node_size = 2000, node_color =  [ca.get(node, 0.25) for node in G.nodes()])
    plt.show()