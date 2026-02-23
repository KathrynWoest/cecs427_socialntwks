# CECS 427 Project 2: Social Networks
Completed By: Kathryn Woest (030131541) and Grace Flores (030169163)


## Usage Instructions
**NOTE:** `plot.py` and `animation.py` rely on a command that is not compatible with WSL. This command automatically opens up the graph's visualizations and animations. If you are unable to use a different terminal like Powershell, comment out `plot.py`'s lines 162-164 and `animation.py`'s line 106 and instead manually open the generated `.html` files through your file explorer.

1. Clone this repo and open it on your IDE

2. DEPENDENCIES: This program relies on four external libraries. To install them, ensure you are inside the project directory and run these commands:
    1. **NetworkX**, a library that provides `.gml` file parsing and writing, graph support, and analysis functions. To install, run: `pip install networkx[default]`
    2. **Scipy**, a math library that provides t-test tables. To install, run: `pip install scipy`
    3. **Plotly**, a library used for creating and plotting graphs. To install, run: `pip install plotly`
    4. **Pandas**, a library used for animation and csv files. To install, run: `pip install pandas`

3. Run this program with: `python graph_analysis.py input_file.gml --components n --split_output_dir --robustness_check k --verify_homophily --verify_balanced_graph --simulate_failures k --clustering a1 --neighborhood a1 a2 --output output_file.gml --plot [C|N|P] --temporal_simulation sim_file.csv`
    1. The first argument after `python graph_analysis.py` MUST be `input_file.gml`.
    2. All other arguments can be provided in any order. For example, `python graph_analysis.py input_file.gml --plot --clustering a1 --verify_homophily` will return the same results as `python graph_analysis.py input_file.gml --clustering a1 --verify_homophily --plot`
    3. However, parameters to those arguments must follow the arguments. For example, `--neighborhood` MUST be directly followed by two starting nodes `a1 a2` or the command will be skipped and an error message printed
    4. With the exception of `input_file.gml`, all other commands are optional. For example, you could just input and simulate failures on a graph with no plotting, verifying balance, or writing to an output file


## Implementation Description
1. **Overall Program:** `graph_analysis.py` calls functions from all the below files to compute things like homophily, balance, and clustering coefficients, and to plot/animate information as well. It also calls functions to parse in a given `.gml` file and write the final graph to another file.
2. **MAIN - graph_analysis.py:** Calls functions from all other files. Allows for arguments to be in any order, as described above. Robust error handling that prevents an error in one function call to crash the entire program (aka will print an error message and then continue executing all other function calls). A lot of code in this file is reused from `graph.py` in Project 1.
3. **animation.py:**
4. **balanced_graph.py:** Defines three functions. `create_supernodes()` creates a list of all the supernodes (as defined in class) in the given graph. `create_supernodes_graph()` takes the supernodes list and generates a graph with the appropriate negative edges between them. `verify_bal()` checks that all the edges are '+' or '-'. calls the above two functions, then utilizes a BFS approach with the supernodes graph to determine if the original graph is balanced and prints the results.
5. **cluster.py:** Determines what the clustering coefficient is for a given node in the graph. Finds all of the node's neighbors, determines the number of edges among them, and then divides that by the number of possible edges to find the coefficient. Saves the coefficient as an attribute to the node it was calculated on.
6. **components.py:**
7. **file_io.py:** Defines two functions. `parse_graph()` takes a `.gml` file in and parses it into a NetworkX graph. `save_graph()` takes the NetworkX graph with any saved results and writes it to a `.gml` file. Reuses a lot of code from `file_io.py` in Project 1.
8. **homophily.py:** Determines if homophily exists in the graph. First checks to see if the graph nodes contain a color attribute. Then calculates the number of cross-edges, all variables needed for a t-test, then utilizes the t-test to see if evidence of homophily exists in the graph.
9. **neighborhood.py:** Calculates the neighborhood overlap for two given nodes in the graph. Finds the number of neighbors shared by them, then divides by the total number of neighbors to find the overlap. Saves the overlap as an attribute to both nodes it was calculated on.
10. **plot.py:**
11. **robustness_check.py:**
12. **simulate_fails.py:** Defines two functions. `removal()` creates a deepcopy of the original graph and removes k random edges from the copy. `failures()` calls `removal()` and then calculates the average shortest path (using BFS), the number of components, and the betweenness centrality on both the original and reduced graph, then analyzes the differences between them.


## Example Commands and Outputs
1. Command: `python3 graph_analysis.py homophily.gml --verify_homophily --components 4 --clustering 3`
2. Command: `python3 graph_analysis.py imbalanced_graph.gml --plot P --verify_balanced_graph --simulate_failures 4`
3. Command: `python3 graph_analysis.py balanced_graph.gml --output test_output.gml --robustness_check 5 --neighborhood 2 4`

Outputs for all are annotated in this PDF: https://pdflink.to/904b5c41/