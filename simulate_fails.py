import networkx as nx
import random
import copy


def removal(graph, k):
    """Function that removes k random edges from user graph
    Inputs: user graph, value k that represents the number of edges to remove
    Output: deepcopy of user graph with k random edges removed"""

    # ensure k is an integer
    try:
        k = int(k)
    except:
        print(f"{k} is not able to be converted into an integer, so removal of k edges is not possible. Simulating failures terminated.\n---")
        return
    
    try:
        # if k is larger than the number of edges, reduce k down to the number of edges (as impact will be the same) to prevent errors in the removal process below
        if k > len(graph.edges()):
            k = len(graph.edges())
        
        # create a deepcopy of the graph to modify
        reduced_graph = copy.deepcopy(graph)

        # create a list of k random numbers between 0 and the number of edges to represent which edges will be removed
        random_edges = []
        for i in range(k):
            num = random.randint(0, len(graph.edges()) - 1)
            while num in random_edges:
                num = random.randint(0, len(graph.edges()) - 1)
            random_edges.append(num)
        
        # place the edges into a list to easily associate them with random_edges
        edges_init = list(enumerate(graph.edges()))
        edges = [e for id, e in edges_init]

        # remove the randomly selected edges
        for edge in random_edges:
            u, v = edges[edge]
            reduced_graph.remove_edge(u, v)

        # return the reduced graph
        return reduced_graph
    
    except Exception as e:
        print(f"Something went wrong in the removal of {k} edges in the failure simulation. Simulation of failure terminated. Error message:", e, "\n---")
        return


def failures(graph, k):
    """Function that determines how the removal of k random edges impacts shortest path, components, and betweenness
    Inputs: user graph, value k that represents the number of edges to remove
    Output: N/A, all print statements"""

    try:
        # remove k random edges from graph
        reduced_graph = removal(graph, k)

        print(f"ANALYSIS: impact of the removal of {k} edges on the graph's average shortest path, connected components, and betweenness.")
        
        # calculate shortest path before and after
        ave_sp_graph = 0
        ave_sp_reduced_graph = 0
        for node in graph.nodes():
            # calculate the length of the longest shortest path from each node to the end of the graph based on BFS traversal
            ave_sp_graph += (len(list(enumerate(nx.bfs_layers(graph, node)))) - 1)
            # the nodes stay the same in reduced_graph, so we can do this calculation in the for-loop too
            ave_sp_reduced_graph += (len(list(enumerate(nx.bfs_layers(reduced_graph, node)))) - 1)

        # average out all the shortest paths in each graph by dividing by the number of nodes
        ave_sp_graph /= len(graph.nodes())
        ave_sp_reduced_graph /= len(graph.nodes())

        if ave_sp_graph > ave_sp_reduced_graph:
            print(f"The average shortest path decreased by {(ave_sp_graph - ave_sp_reduced_graph):.2f}, from {ave_sp_graph:.2f} in the original graph to {ave_sp_reduced_graph:.2f} in the reduced graph.")
        elif ave_sp_reduced_graph > ave_sp_graph:
            print(f"The average shortest path increased by {(ave_sp_reduced_graph - ave_sp_graph):.2f}, from {ave_sp_graph:.2f} in the original graph to {ave_sp_reduced_graph:.2f} in the reduced graph.")
            print(f"The average shortest path in the reduced graph is {ave_sp_reduced_graph:.2f}, which increased by {(ave_sp_reduced_graph - ave_sp_graph):.2f} from the average shortest path in the original graph of {ave_sp_graph:.2f}.")
        else:
            print(f"The average shortest path remained the same between the removal of {k} edges, staying at {ave_sp_graph:.2f}.")

        # calculate the number of disconnected components
        connected_comp_graph = nx.number_connected_components(graph)
        connected_comp_reduced_graph = nx.number_connected_components(reduced_graph)

        if connected_comp_graph < connected_comp_reduced_graph:
            print(f"The components disconnected, from {connected_comp_graph} components in the original graph to {connected_comp_reduced_graph} components in the reduced graph.")
        else:
            print(f"No components disconnected, staying at {connected_comp_graph} components after the removal of {k} edges.")

        # calculate the impact on betweenness centrality
        # determine the betweenness for each node, then flatten into a list and average the values
        betweenness_graph_init = nx.betweenness_centrality(graph, None, True)
        betweenness_graph_vals = list(betweenness_graph_init.values())
        betweenness_graph = sum(betweenness_graph_vals) / len(betweenness_graph_vals)

        betweenness_reduced_graph_init = nx.betweenness_centrality(reduced_graph, None, True)
        betweenness_reduced_graph_vals = list(betweenness_reduced_graph_init.values())
        betweenness_reduced_graph = sum(betweenness_reduced_graph_vals) / len(betweenness_reduced_graph_vals)

        if betweenness_graph > betweenness_reduced_graph:
            print(f"The betweenness centrality decreased by {(betweenness_graph - betweenness_reduced_graph):.3f}, from {betweenness_graph:.3f} in the original graph to {betweenness_reduced_graph:.3f} in the reduced graph.\n---")
        elif betweenness_reduced_graph > betweenness_graph:
            print(f"The betweenness centrality increased by {(betweenness_reduced_graph - betweenness_graph):.3f}, from {betweenness_graph:.3f} in the original graph to {betweenness_reduced_graph:.3f} in the reduced graph.\n---")
        else:
            print(f"The betweenness centrality did not change after the removal of {k} edges, remaining at {betweenness_graph:.3f}.\n---")
        
    except Exception as e:
        print("Something went wrong in the simulation of failure. Simulation of failure terminated. Error message:", e, "\n---")
        return
