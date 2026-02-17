import networkx as nx
import itertools

def components(n, graph):
    # girvan_newman() returns an interator that yields a sequence of communities at each level
    communities_iterator = nx.community.girvan_newman(graph)

    # number of components
    n = n

    # stop the iteration when number of communities exceeds n (yields tuples of sets)
    n_iterations = itertools.takewhile(lambda c: len(c) <= n, communities_iterator)

    # take the last result (the partition with n components, less than n if n exceeds maximum number of components for the graph)
    partition = None
    for communities in n_iterations:
        partition = communities
    
    print(f"Graph partitioned into {len(partition)} components:")
    for i, comm in enumerate(partition):
        print(f"  Component {i+1}: {comm}")
    else:
        print(f"Could not find a partition with exactly {n} components within the algorithm's steps, or graph has fewer than {n} components initially.")
    return