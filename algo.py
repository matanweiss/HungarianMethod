import networkx as nx
import matplotlib.pyplot as plt


def createGraph(GraphAsMatrix, M):
    # Create a directed graph
    G = nx.DiGraph()
    # Create A's vertices
    for i in range(len(GraphAsMatrix)):
        G.add_node('A'+str(i), bipartite='A', isMatched=False)
    # Create B's vertices
    for i in range(len(GraphAsMatrix[0])):
        G.add_node('B'+str(i),  bipartite='B', isMatched=False)

    # Add all the edeges according to the given matrix
    for i in range(len(GraphAsMatrix)):
        for j in range(len(GraphAsMatrix[0])):
            if GraphAsMatrix[i][j]:
                u, v = 'A'+str(i), 'B'+str(j)
                # Check if the edege is in the matching list
                if (u, v) in M:
                    G.add_edge(v, u, color='lightcoral')
                    G.nodes[u]['isMatched'] = True
                    G.nodes[v]['isMatched'] = True

                else:
                    G.add_edge(u, v, color='lightblue')
    return G


def augmentGraph(G, M, GraphAsMatrix):
    # 1 edge path
    for (u, v) in G.edges:
        # check if u, v vertices are not mathched
        if not G.nodes[u]['isMatched'] and not G.nodes[v]['isMatched']:
            # add the edge (u,v) to the Matching list
            M.append((u, v))

            # update the Nodes attritubes
            G.nodes[u]['isMatched'] = True
            G.nodes[v]['isMatched'] = True

            # change the edge direction and color
            G.remove_edge(u, v)
            G.add_edge(v, u, color='lightgreen')
            showGraph(G, GraphAsMatrix)
            G.edges[(v, u)]['color'] = 'lightcoral'

            # we found an augment match
            return True

    # 3 edges path
    for (a, b) in M:
        # Check the neighbors of vertex a
        neighborsOfA = [n for n in G.neighbors(a)]
        # check if a has neighbors
        if not neighborsOfA:
            continue

        # check if b has neighbor that not in the Matching list
        for i in range(len(GraphAsMatrix)):
            if GraphAsMatrix[i][int(b[1:])] and not G.nodes['A'+str(i)]['isMatched']:

                # update the Matching list
                M.remove((a, b))
                M.append((a, neighborsOfA[0]))
                M.append(('A'+str(i), b))

                # update the Nodes attritubes
                G.nodes[neighborsOfA[0]]['isMatched'] = True
                G.nodes['A'+str(i)]['isMatched'] = True

                # change the edge direction and color
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

                # we found an augment match
                return True

    # we didn't find an augment match
    return False


def findMaximumMatching(G, M, GraphAsMatrix):
    # while we have an augment match keep running
    while augmentGraph(G, M, GraphAsMatrix):
        pass
    # Show the final matching
    showGraph(G, GraphAsMatrix)


def showGraph(G, GraphAsMatrix):
    # define an array of the edges colors
    edge_colors = [G.edges[edge]['color'] for edge in G.edges]

    # define an array of the vertices colors - decide the color in accordance to whether the node is matched or not
    node_colors = ['lightcoral' if G.nodes[node]
                   ['isMatched'] else 'lightblue' for node in G.nodes]
    
    # splitting the graph to appear bipartite
    pos = nx.bipartite_layout(G, ['A'+str(i)
                              for i in range(len(GraphAsMatrix[0]))])
    
    # drawing the graph
    nx.draw_networkx(G, pos, with_labels=True,
                     node_color=node_colors, edge_color=edge_colors, arrows=True)
    
    # setting the plot to non-blocking so we can update the graph with the algorithm
    plt.ion()
    
    # show the graph in a pop-up window
    plt.show()
    
    # wait before continuing to the next iteration
    plt.pause(2)

