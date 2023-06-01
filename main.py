from algo import createGraph, findMaximumMatching, showGraph

if __name__ == "__main__":

    # define the Matching list
    M = [('A1', 'B3')]

    # define Adjacency matrix
    G = [
        [0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0]
    ]

    # create the graph according to the Adjacency matrix
    Graph = createGraph(G, M)
    
    # show the input graph and matching
    showGraph(Graph, G)
    
    # start the maximun match according to the Hungarian Method
    findMaximumMatching(Graph, M, G)
