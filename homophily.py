import networkx as nx
import scipy.stats as ss


def verify_hom(graph):
    """Function that determines whether color-coded homophily exists in the graph using a statistical t-test
    Input: user graph
    Output: boolean - True if homophily exists, False if not"""

    # check if one of the nodes doesn't have a color attribute. if one is missing, terminate the program.
    for node, color in graph.nodes(data="color"):
        if color == None:
            raise Exception("At least one node in the graph does not contain a 'color' field, so homophily cannot be calculated. Program terminated.")
    
    try:
        # determine the number of cross edges
        color_list = list(nx.get_node_attributes(graph, 'color').values())
        c1 = color_list[0]
        
        total_edges = len(graph.edges)
        cross_edges = 0

        for node1, node2 in graph.edges():
            if graph.nodes[node1]["color"] != graph.nodes[node2]["color"]:
                cross_edges += 1
        
        # calculate variables: number of nodes, degrees of freedom, p, mu, mu0, and sigma0
        n = len(color_list)
        df = n - 1
        p = color_list.count(c1)/n
        q = 1 - p
        mu = cross_edges / total_edges
        mu0 = 2 * p * q
        sigma0 = mu0 * (1 - (2 * p * (1 - p)))
        
        # calculate the t-test table value and the value to test against it
        table_value = ss.t.ppf(0.95, df)
        test_value = (abs(mu - mu0) * (n ** (1/2))) / sigma0
    
    except Exception as e:
        raise Exception("Something went wrong in the calculation of homophily. Program terminated. Error message:", e)

    # determine if the difference is statistically significant or not
    if test_value > table_value:
        print(f"The graph has evidence of homophily, with {mu:.2f} [the fraction of cross-edges] being significantly less than {mu0:.2f} [2p(1-p)].")
        return True
    
    else:
        print(f"The graph does not have evidence of homophily, with {mu:.2f} [the fraction of cross-edges] not being significantly less than {mu0:.2f} [2p(1-p)].")
        return False
