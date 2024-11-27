def get_grapgh_from_file(filename, graph: dict[str, list]):
    with open(filename, "r") as f:
        n = f.readline()  # noqa: F841
        vertexes = f.readline().split()
        edges = []
        e = f.readline()
        while e!="":
            edges.append([vertexes.index(edge) for edge in e.split()])
            e = f.readline()
    for i in range(len(vertexes)):
        graph[i] = []
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return vertexes

def is_tree(graph, n):
    visited = [False] * n
    cycle = None  

    def iterative_dfs(start):
        nonlocal cycle
        visited_start = [False] * n
        
        stack = [(start, None)]
        path = []  

        while stack:
            node, parent = stack.pop()

            if not visited_start[node]:
                visited_start[node] = True
                path.append(node)  

                for neighbor in graph[node]:
                    if not visited_start[neighbor]:
                        stack.append((neighbor, node))
                    elif neighbor != parent and cycle is None:
                        cycle_start = path.index(neighbor)
                        cycle = path[cycle_start:] + [neighbor]

            while path and path[-1] == node and all(visited_start[nb] for nb in graph[node]):
                path.pop()
        return visited_start

    components = []
    visited = iterative_dfs(0)
    components.append([i for i in range(n) if visited[i]])
    for v in range(n):
        if not visited[v]:
            components.append([i for i in range(n) if iterative_dfs(v)[i]])

    k = len(components)
    z = 1 if cycle else 0  
    q = sum(len(edges) for edges in graph.values()) // 2

    if k == 1 and z == 0:
        result = "Граф является деревом."
        result += " Он также древочисленный." if q == n - 1 else " Он не древочисленный."
    else:
        result = "Граф не является деревом.\n"
        if k > 1:
            result += f"Нарушена связность: {k} компонент(ы) связности: {components}.\n"
        if z > 0:
            result += f"Обнаружен цикл: {cycle}.\n"
        result += "Граф " + ("является" if q == n - 1 else "не является") + " древочисленным."
    
    return result

# Пример использования
graph: dict[int, list] = {}
vertexes = get_grapgh_from_file(input("Filename of graph: "), graph)

print(is_tree(graph, len(vertexes)))
