import networkx as nx
import copy


def create_supernodes(graph, node_list, supernode_list, iterator):
    """Function that splits a graph into supernodes by picking a node and placing all the nodes with a positive edge into the same supernode, then removing all those nodes from the graph and repeating until all nodes are partitioned
    Inputs: user graph, the list of all the nodes remaining in the graph, the list of supernodes (each supernode represented by a list of the nodes in it), and an iterator that tracks which supernode is being filled
    Outputs: the updated node list (with nodes moved into a supernode removed) and the updated supernode list (with nodes moved into a supernode added)"""

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


def verify_bal(graph):
    """Function that determines if a graph is balanced using the BFS algorithm
    Input: user graph
    Output: boolean - True if balanced, False if not"""

    # check if one of the edges doesn't have a sign attribute. if one is missing, terminate the program.
    for node1, node2, sign in graph.edges(data="sign"):
        if sign == None or sign not in ["+", "-"]:
            raise Exception("At least one edge in the graph does not contain a 'sign' field or the value is not '-' or '+', so balance cannot be calculated. Program terminated.")

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
        # increment the supernode tracker to restart with the new first node
        i += 1
