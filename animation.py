import networkx as nx
import pandas as pd
import plotly.graph_objects as go


def animation(csv_path):

    # Load CSV
    df = pd.read_csv(csv_path)
    df = df.sort_values("timestamp")

    G = nx.Graph()

    frames = []

    timestamps = sorted(df["timestamp"].unique())

    for t in timestamps:

        # Apply all changes at time t
        changes = df[df["timestamp"] == t]

        for _, row in changes.iterrows():
            u = row["source"]
            v = row["target"]
            action = row["action"]

            if action == "add":
                G.add_edge(u, v)
            elif action == "remove":
                if G.has_edge(u, v):
                    G.remove_edge(u, v)

        # Compute layout (spring layout keeps positions stable)
        all_nodes = set(df["source"]).union(set(df["target"]))
        G.add_nodes_from(all_nodes)
        pos = nx.spring_layout(G, seed=42)

        # Build edge trace
        edge_x, edge_y = [], []
        for u, v in G.edges():
            edge_x += [pos[u][0], pos[v][0], None]
            edge_y += [pos[u][1], pos[v][1], None]

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=1, color="#888"),
            hoverinfo="none"
        )

        # Build node trace
        node_x = [pos[n][0] for n in G.nodes()]
        node_y = [pos[n][1] for n in G.nodes()]

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=list(G.nodes()),
            textposition="top center",
            marker=dict(size=10, color="blue"),
        )

        # Create frame
        frames.append(
            go.Frame(
                data=[edge_trace, node_trace],
                name=str(t)
            )
        )

    # Initial graph state
    fig = go.Figure(
        data=frames[0].data,
        frames=frames
    )

    # Add animation controls
    fig.update_layout(
        title="Temporal Network Evolution",
        updatemenus=[
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 800, "redraw": True}}]
                    }
                ]
            }
        ],
        sliders=[{
            "steps": [
                {
                    "method": "animate",
                    "args": [[str(t)], {"frame": {"duration": 800, "redraw": True}}],
                    "label": str(t)
                } for t in timestamps
            ]
        }]
    )

    fig.show()