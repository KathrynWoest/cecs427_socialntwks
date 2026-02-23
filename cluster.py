import networkx as nx


def clustering_coefficient(graph, node):
    """Function that calculates the clustering coefficient of the given node in a graph, then saves that value with the node in the graph
    Inputs: user graph, selected node to perform calculation on
    Output: N/A - all print statements"""

    # check to ensure the desired node exists in the graph
    if not graph.has_node(node):
        print(f"Graph does not contain node '{node}', so clustering coefficient can't be calculated. Calculation of clustering coefficient terminated.\n---")
        return

    try:
        # place all of the node's neighbors in a list
        all_neighbors = list(enumerate(graph.neighbors(node)))
        neighbors = [node for id, node in all_neighbors]

        # the possible edges must be a positive number, so if the number of neighbors is 0 or 1, the coefficient can't be calculated
        # return -1, to represent a non-existent coefficient (since 0 is possible)
        if len(neighbors) == 0:
            print(f"Node '{node}' has no neighbors, so clustering coefficient cannot be calculated.\n---")
            return
        elif len(neighbors) == 1:
            print(f"Node '{node}' has only one neighbor, so clustering coefficient cannot be calculated.\n---")
            return
        
        # calculate the number of possible edges among node's neighbors
        possible_edges = (len(neighbors) * (len(neighbors) - 1)) / 2
        
        # calculate the number of actual edges among node's neighbors
        actual_edges = 0
        tracker = []

        # iterate through the neighbors and pull their edges
        for n in neighbors:
            edges = graph.edges(n)
            # for each edge connected to a neighbor
            for n1, n2 in edges:
                # if the edge is connected to another neighbor and has not already been counted
                if (n1 in neighbors) and (n2 in neighbors) and (n1 != node) and (n2 != node) and ([n1, n2] not in tracker) and ([n2, n1] not in tracker):
                    # count the edge
                    tracker.append([n1, n2])
                    actual_edges += 1
        
        # calculate clustering coefficient, save it into the node in the graph, and print/return the results
        coefficient = actual_edges / possible_edges
        graph.nodes[node]["clustering_coefficient"] = coefficient
        print(f"The clustering coefficient of node '{node}' is: {coefficient:.2f}.\n---")
        return coefficient
    
    except Exception as e:
        print("Something went wrong in the calculation of the clustering coefficient. Calculation of clustering coefficient terminated. Error message:", e, "\n---")
        return
