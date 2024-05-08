import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue

class Ordered_Node:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description

    def __lt__(self, other):  # Use __lt__ for Python 3.x
        return self.priority < other.priority

def getPriorityQueue(lst, heuristics):
    pq = PriorityQueue()
    for node in lst:
        pq.put(Ordered_Node(heuristics[node], node))
    return pq

def BFSUtil(G, v, visited, final_path, dest, goal):
    if goal == 1:
        return goal
    visited[v] = True
    final_path.append(v)
    if v == dest:
        goal = 1
    else:
        pq = getPriorityQueue(G[v], heuristics)
        while not pq.empty():
            i = pq.get().description
            if goal != 1 and not visited[i]:
                goal = BFSUtil(G, i, visited, final_path, dest, goal)
    return goal

def BFS(G, source, dest, heuristics, pos):
    visited = {node: False for node in G.nodes()}
    final_path = []
    goal = BFSUtil(G, source, visited, final_path, dest, 0)
    prev = -1
    for var in final_path:
        if prev != -1:
            curr = var
            nx.draw_networkx_edges(G, pos, edgelist=[(prev, curr)], width=2.5, alpha=0.8, edge_color='black')
            prev = curr
        else:
            prev = var
            return

def getHeuristics(G):
    heuristics = {}
    with open('heuristics.txt') as f:
        for line in f:
            node, heuristic_val = line.split()
            heuristics[node] = int(heuristic_val)  # Convert heuristic_val to int
    return heuristics

def CreateGraph():
    G = nx.Graph()
    with open('input.txt') as f:
        n = int(f.readline())
        for _ in range(n):
            node1, node2, length = f.readline().split()
            G.add_edge(node1, node2, length=length)
        source = f.readline().strip()  # Use strip() to remove newline characters
        dest = f.readline().strip()
    return G, source, dest

def DrawPath(G, source, dest):
    pos = nx.spring_layout(G)
    val_map = {source: 'green', dest: 'red'}
    values = [val_map.get(node, 'blue') for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=values, edge_color='b', width=1, alpha=0.7)
    edge_labels = {(u, v): d['length'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5, font_size=11)
    return pos

if __name__ == "__main__":
    G, source, dest = CreateGraph()
    heuristics = getHeuristics(G)
    pos = DrawPath(G, source, dest)
    BFS(G, source, dest, heuristics, pos)
    plt.show()

