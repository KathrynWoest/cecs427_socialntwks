import networkx as nx


def neighborhood_overlap(graph, node1, node2, plot=False):
    """Function that calculates the neighborhood overlap between node1 and node2, then saves that information with the nodes in the graph
    Inputs: user graph, two nodes to perform the calculation on, boolean to check if being used for plotting
    Output: N/A - all print statements"""

    # check to ensure the desired nodes exist in the graph
    if not graph.has_node(node1) or not graph.has_node(node2):
        print(f"Graph does not contain node '{node1}' and/or '{node2}', so neighborhood overlap can't be calculated. Neighborhood overlap calculation terminated.\n---")
        return
    
    try:
        # place all of the nodes' neighbors in lists and remove node1 and node2 from those lists
        all_neighbors_1 = list(enumerate(graph.neighbors(node1)))
        all_neighbors_2 = list(enumerate(graph.neighbors(node2)))
        neighbors_1 = [node for id, node in all_neighbors_1 if node != node2]
        neighbors_2 = [node for id, node in all_neighbors_2 if node != node1]

        if len(neighbors_1) == 0 or len(neighbors_2) == 0:
            print(f"Nodes '{node1}' and/or '{node2}' have no neighbors, so cannot calculate neighborhood overlap.\n---")
            return

        # calculate OR nodes
        or_nodes = len(neighbors_1)
        for node in neighbors_2:
            if node not in neighbors_1:
                or_nodes += 1

        # calculate AND nodes
        and_nodes = 0
        for node in neighbors_1:
            if node in neighbors_2:
                and_nodes += 1
        
        # calculate neighborhood overlap, save it into the nodes in the graph, and print/return the results
        overlap = and_nodes / or_nodes
        graph.nodes[node1]["neighborhood_overlap"] = f"{node2}, {overlap}"
        graph.nodes[node2]["neighborhood_overlap"] = f"{node1}, {overlap}"
        if not plot:
            print(f"The neighborhood overlap of nodes '{node1}' and '{node2}' is: {overlap:.2f}.\n---")
        return overlap
        
    except Exception as e:
        print("Something went wrong in the calculation of neighborhood overlap. Calculation of neighborhood overlap terminated. Error message:", e, "\n---")
        return
