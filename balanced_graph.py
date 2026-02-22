import networkx as nx


def create_supernodes(graph, node_list, supernode_list, iterator):
    """Function that splits a graph into supernodes by picking a node and placing all the nodes with a positive edge into the same supernode, then removing all those nodes from the graph and repeating until all nodes are partitioned
    Inputs: user graph, the list of all the nodes remaining in the graph, the list of supernodes (each supernode represented by a list of the nodes in it), and an iterator that tracks which supernode is being filled
    Outputs: the updated node list (with nodes moved into a supernode removed) and the updated supernode list (with nodes moved into a supernode added)"""

    try:
        # pick the comparative node to be the first in the list, add it into a supernode, then remove it from the node list
        start_node = node_list[0]
        supernode_list[iterator].append(start_node)
        node_list.remove(start_node)

        # iterate through all the edges
        for node1, node2, sign in graph.edges(data="sign"):
            # if the edge contains the start/comparative node and the other node connected by the edge is not already in the supernode...
            if (node1 == start_node and node2 not in supernode_list[iterator]) or (node2 == start_node and node1 not in supernode_list[iterator]):
                # check to see if the edge is positive
                if sign == "+":
                    # if it is, add the non-comparative node into the supernode and remove it from the node list
                    if node1 == start_node:
                        supernode_list[iterator].append(node2)
                        node_list.remove(node2)  # we know we can remove because we checked for its existence before reaching this statement
                    else:
                        supernode_list[iterator].append(node1)
                        node_list.remove(node1)
        
        # now iterate through the supernode list and repeat the process with each node as the comparative node to find any nodes connected positively to a node in the supernode that weren't connected to the initial comparative node
        for node in supernode_list[iterator]:
            # if the node is the initial comparative node, then we just did the process above, so skip it
            if node != start_node:
                new_start_node = node

                # repeat the above calculations
                for node1, node2, sign in graph.edges(data="sign"):
                    if (node1 == new_start_node and node2 not in supernode_list[iterator]) or (node2 == new_start_node and node1 not in supernode_list[iterator]):
                        if sign == "+":
                            if node1 == new_start_node:
                                supernode_list[iterator].append(node2)
                                node_list.remove(node2)
                            else:
                                supernode_list[iterator].append(node1)
                                node_list.remove(node1)

        # return the updated lists
        return node_list, supernode_list
    
    except Exception as e:
        print("Something went wrong in the creation of supernodes in trying to determine the if the graph is balanced. Calculation of balance terminated. Error message:", e, "\n---")
        return


def create_supernodes_graph(graph, supernode_list):
    """Function that takes the user graph and the list of the supernodes in it, then constructs a graph with the supernodes and edges connecting them
    Input: user graph and the list of supernodes (formatted as [[supernode1], [supernode2], ...])
    Output: the constructed supernode graph"""

    try:
        supernode_graph = nx.empty_graph()
        j = 0

        # add nodes, labeled 0, 1, 2, ...
        for supernode in supernode_list:
            supernode_graph.add_node(j, label=j)
            j += 1

        # make a list of all the negative edges in the graph
        negative_edges = []
        for node1, node2, sign in graph.edges(data="sign"):
            if sign == "-":
                negative_edges.append([node1, node2])
        
        # add edges
        for i in range(len(supernode_list)):
            # iterate through each supernode in the supernodes list
            supernode = supernode_list[i]
            for edge in negative_edges:
                # for each possible negative edge, check to see if it has an end node in the supernode
                if (edge[0] in supernode and edge[1] not in supernode) or (edge[0] not in supernode and edge[1] in supernode):
                    # check which node is not in the current supernode
                    if edge[0] not in supernode:
                        diff_node = edge[0]
                    else:
                        diff_node = edge[1]

                    # then iterate through the supernodes to find which one it does belong to
                    diff_supernode = i
                    for j in range(len(supernode_list)):
                        if diff_node in supernode_list[j]:
                            diff_supernode = j

                    # check if the edge from the current supernode to the supernode the other node is in exists in the supernode graph
                    if not supernode_graph.has_edge(i, diff_supernode) or not supernode_graph.has_edge(diff_supernode, i):
                        # if it's not, add the edge
                        supernode_graph.add_edge(i, diff_supernode)
    
        # return the generated supernode graph
        return supernode_graph
    
    except Exception as e:
        print("Something went wrong in the creation of a supernode graph in trying to determine the if the graph is balanced. Calculation of balance terminated. Error message:", e, "\n---")
        return


def verify_bal(graph):
    """Function that determines if a graph is balanced using the BFS algorithm
    Input: user graph
    Output: N/A, all print statements"""

    # check if one of the edges doesn't have a sign attribute. if one is missing, terminate the program.
    for node1, node2, sign in graph.edges(data="sign"):
        if sign == None or sign not in ["+", "-"]:
            print("At least one edge in the graph does not contain a 'sign' field or the value is not '-' or '+', so balance cannot be calculated. Calculating balance terminated.\n---")
            return

    try:
        # create a list of all the nodes, an empty list to keep track of the supernodes, and an iterator to keep track of which supernode is being added to
        nodes = list(graph.nodes)
        supernodes = []  # to be structured as [[supernode1], [supernode2], ...]
        i = 0

        # while there are still nodes to partition into a supernode...
        while len(nodes) > 0:
            # add a new supernode into the list
            supernodes.append([])
            # partition all of the nodes that match the first node in nodes into the above supernode
            nodes, supernodes = create_supernodes(graph, nodes, supernodes, i)

            # check if supernodes contain negative edges in them
            for node1, node2, sign in graph.edges(data="sign"):
                # if both nodes connected by a negative edge are in the supernode, then return False
                if node1 in supernodes[i] and node2 in supernodes[i] and sign == "-":
                    print("The graph is unbalanced.\n---")
                    return

            # increment the supernode tracker to restart with the new first node if the supernode contains no negative edges
            i += 1

        # create the supernode graph with the negative edges between them
        supernode_graph = create_supernodes_graph(graph, supernodes)

        # create a list of the layers of nodes for a BFS search from the first node in the list
        bfs_list = list(enumerate(nx.bfs_layers(supernode_graph, supernode_graph.nodes[0]["label"])))

        # go through each layer in the BFS traversal
        for layer, nodes in bfs_list:
            # check between every node in the layer for an edge
            for i in range(len(nodes)):
                if i + 2 <= len(nodes):
                    if supernode_graph.has_edge(nodes[i], nodes[i+1]) or supernode_graph.has_edge(nodes[i+1], nodes[i]):
                        # if an edge exists, return False
                        print("The graph is unbalanced.\n---")
                        return
        
        # if this point is reached, then there are no negative edges within supernodes or edges between nodes in the same level from a BFS search, so the graph is balanced. return True
        print("The graph is balanced.\n---")
    
    except Exception as e:
        print("Something went wrong in trying to determine the if the graph is balanced. Calculation of balance terminated. Error message:", e, "\n---")
        return
