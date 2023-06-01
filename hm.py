import networkx as nx
import matplotlib.pyplot as plt


def createGraph(GraphAsMatrix, M):
    # Create a directed graph
    G = nx.DiGraph()
    # Create A's vertexes
    for i in range(len(GraphAsMatrix)):
        G.add_node('A'+str(i), bipartite='A', isMatched=False)
    # Create B's vertexes
    for i in range(len(GraphAsMatrix[0])):
        G.add_node('B'+str(i),  bipartite='B', isMatched=False)

    # Add all the edeges according to the given matrix
    for i in range(len(GraphAsMatrix)):
        for j in range(len(GraphAsMatrix[0])):
            if GraphAsMatrix[i][j]:
                u, v = 'A'+str(i), 'B'+str(j)
                #Check if the edege is in the matching list 
                if (u, v) in M:
                    G.add_edge(v, u, color='lightcoral')
                    G.nodes[u]['isMatched'] = True
                    G.nodes[v]['isMatched'] = True

                else:
                    G.add_edge(u, v, color='lightblue')
    return G


def augmentGraph(G, M, GraphAsMatrix):
    for (u, v) in G.edges:
        if not G.nodes[u]['isMatched'] and not G.nodes[v]['isMatched']:
            # add the edge (u,v) to the Matching list
            M.append((u, v))

            # update the Nodes attritubes
            G.nodes[u]['isMatched'] = True
            G.nodes[v]['isMatched'] = True

            # change the edge direction
            G.remove_edge(u, v)
            G.add_edge(v, u, color='lightgreen')
            showGraph(G, GraphAsMatrix)
            G.edges[(v,u)]['color'] = 'lightcoral'

            return True

    for (a, b) in M:
        neighborsOfA = [n for n in G.neighbors(a)]
        if not neighborsOfA:
            continue
        #  = neighborsOfA[0]
        for i in range(len(GraphAsMatrix)):
            if GraphAsMatrix[i][int(b[1:])] and not G.nodes['A'+str(i)]['isMatched']:

                # update the Matching list
                M.remove((a, b))
                M.append((a, neighborsOfA[0]))
                M.append(('A'+str(i), b))

                # update the nodes
                G.nodes[neighborsOfA[0]]['isMatched'] = True
                G.nodes['A'+str(i)]['isMatched'] = True

                # update the edges
                G.remove_edge(b, a)
                G.add_edge(a, b, color='green')
                G.remove_edge(a, neighborsOfA[0])
                G.add_edge(neighborsOfA[0], a, color='lightgreen')
                G.remove_edge('A'+str(i), b)
                G.add_edge(b, 'A'+str(i), color='lightgreen')
                showGraph(G, GraphAsMatrix)
                G.edges[(neighborsOfA[0], a)]['color'] = 'lightcoral'
                G.edges[(b, 'A'+str(i))]['color'] = 'lightcoral'
                G.edges[(a, b)]['color'] = 'lightblue'
                return True
    return False


def findPrefectMatching(G, M, GraphAsMatrix):
    while augmentGraph(G, M, GraphAsMatrix):
        pass
    showGraph(G, GraphAsMatrix)

def showGraph(G, GraphAsMatrix):
    edge_colors = [G.edges[edge]['color'] for edge in G.edges]
    node_colors = ['lightcoral' if G.nodes[node]
                   ['isMatched'] else 'lightblue' for node in G.nodes]
    pos = nx.bipartite_layout(G, ['A'+str(i)
                              for i in range(len(GraphAsMatrix[0]))])
    nx.draw_networkx(G, pos, with_labels=True,
                     node_color=node_colors, edge_color=edge_colors, arrows=True)
    plt.ion()
    plt.show()
    plt.pause(2)


M = [('A1', 'B3')]


G = [
    [0, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0]
]

Graph = createGraph(G, M)
showGraph(Graph, G)
findPrefectMatching(Graph,M,G)
