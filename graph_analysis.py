## NOTE: this file reuses a lot of code from Project 1

import sys
import file_io as fio
import homophily as hom
import balanced_graph as bal
import cluster
import neighborhood as nh
import simulate_fails as sf
import components as comp
import robustness_check as rc
import plot
import animation as anim


def main():
    # get arguments from command line and initialize BFS node list, the end of the argument list, and bools for which analyses were called
    args = sys.argv
    end = len(args)

    # if there are less than 2 arguments, then not possible to do anything. terminate program.
    if end < 2:
        raise Exception(f"Program was terminated because there is no file to upload a graph with.\n---")
    
    # parse in graph from given .gml file
    user_graph = fio.parse_graph(args[1])

    # call the components function
    if "--components" in args:
        # check if the number of components is missing. if so, terminate program.
        if (args.index("--components") + 1 >= end) or ("--" in args[args.index("--components") + 1]):
            print("Calculating components was terminated because it was missing the number of components for partitioning.\n---")
        else:
            n = args[args.index("--components") + 1]
            # check if each component should be exported to a separate .gml file
            if "--split_output_dir" in args:
                comp.components(n, user_graph, True)
            else:
                comp.components(n, user_graph)
            
    # call the robustness check
    if "--robustness_check" in args:
        # check if k is missing. if so, terminate program.
        if (args.index("--robustness_check") + 1 >= end) or ("--" in args[args.index("--robustness_check") + 1]):
            print("Robustness check was terminated because it was missing the number of components for partitioning.\n---")
        else:
            k = args[args.index("--robustness_check") + 1]
            rc.robustness_check(user_graph, k)

    # call the homophily function
    if "--verify_homophily" in args:
        hom.verify_hom(user_graph)

    # call the balanced graph function
    if "--verify_balanced_graph" in args:
        bal.verify_bal(user_graph)

    # call the simulate failures function
    if "--simulate_failures" in args:
        # check if k is missing. if so, terminate program.
        if (args.index("--simulate_failures") + 1 >= end) or ("--" in args[args.index("--simulate_failures") + 1]):
            print("Simulating failures was terminated because it was missing the number of removal edges argument.\n---")
        else:
            k = args[args.index("--simulate_failures") + 1]
            sf.failures(user_graph, k)

    # call the clustering coefficient function
    if "--clustering" in args:
        # check if the selected node is missing. if so, terminate program.
        if (args.index("--clustering") + 1 >= end) or ("--" in args[args.index("--clustering") + 1]):
            print("Clustering coefficient calculation was terminated because it was missing the clustering coefficient node argument.\n---")
        else:
            selected_node = args[args.index("--clustering") + 1]
            cluster_coeff = cluster.clustering_coefficient(user_graph, selected_node)
    
    # call the neighborhood overlap function
    if "--neighborhood" in args:
        # check if the selected nodes are missing. if so, terminate program.
        if (args.index("--neighborhood") + 2 >= end) or ("--" in args[args.index("--neighborhood") + 1]) or ("--" in args[args.index("--neighborhood") + 2]):
            print("Neighborhood overlap calculation was terminated because it was missing the neighborhood overlap nodes arguments.\n---")
        else:
            selected_node_1 = args[args.index("--neighborhood") + 1]
            selected_node_2 = args[args.index("--neighborhood") + 2]

            neighborhood_over = nh.neighborhood_overlap(user_graph, selected_node_1, selected_node_2)

    # call the output function
    if "--output" in args:
        # check if the output file name is missing. if so, terminate program.
        if (args.index("--output") + 1 >= end) or ("--" in args[args.index("--output") + 1]):
            print("Outputting the file was terminated because it was missing the output file name argument.\n---")
        else:
            output_file = args[args.index("--output") + 1]
            fio.save_graph(user_graph, output_file)

    # call the visualization function
    if "--plot" in args:
        # check if vis output control is missing. if so, terminate program.
        if (args.index("--plot") + 1 >= end) or ("--" in args[args.index("--plot") + 1]):
            print("Plotting was terminated because it was missing the plot control argument.\n---")
        else:
            control = args[args.index("--plot") + 1]
            if control not in ["C", "N", "P"]:
                print("Plotting was terminated because the plot control argument was not C, N, or P.\n---")
            else:
                plot.plot(control, user_graph, cluster_coeff, neighborhood_over)
    
    # call the temporal simulation function
    if "--temporal_simulation" in args:
         # check if the simulation file is missing. if so, terminate program.
        if (args.index("--temporal_simulation") + 1 >= end) or ("--" in args[args.index("--temporal_simulation") + 1]):
            print("Temporal simulation was terminated because it was missing the simulation file argument.\n---")
        else:
            sim_file = args[args.index("--temporal_simulation") + 1]
            anim.animation(sim_file)

main()