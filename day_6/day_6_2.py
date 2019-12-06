from sys import argv
def add_edge(graph, v, w):
    if v in graph:
        graph[v].append(w)
    else:
        graph[v] = [w]
    if w in graph:
        graph[w].append(v)
    else:
        graph[w] = [v]

def build_graph(orbit_map):
    graph = {'COM': []}
    nodes = []
    for edge in orbit_map:
        edge = edge.split(")")
        v = edge[0]
        w = edge[1]
        add_edge(graph, v, w)
        if w not in graph:
            graph[w] = []
        if w not in nodes:
            nodes.append(w)
    return (graph, nodes)

def bfs(graph, source):

    queue = []
    marked = {source: True}
    edge_to = {source: None}
    queue.append(source)
    while len(queue) > 0:
        v = queue.pop(0)
        for w in graph[v]:
            if w not in marked:
                edge_to[w] = v
                marked[w] = True
                queue.append(w)

    return (marked, edge_to)

def get_path_to(w, marked, edge_to):

    if w not in marked:
        return (None, 0)
    
    path = [edge_to[w]]
    last = path[0]
    length = 0
    while last is not None:
        path.insert(0, edge_to[last])
        last = path[0]
        length = length + 1
    return (path, length)


if __name__ == "__main__":
    data = None

    with open(argv[1], 'r') as file:
        data = file.read()

    orbit_map = data.split("\n")
    g, nodes = build_graph(orbit_map)
    marked, edge_to = bfs(g, 'YOU')

    path, length = get_path_to('SAN', marked, edge_to)

    print(path, length - 2) #counting the number of orbital transfers 

    