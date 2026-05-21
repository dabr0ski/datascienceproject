import osmnx as ox

print("Downloading Aarhus walking network...")

# Coordinates of aarhus and walkable streets
graph = ox.graph_from_point(
    (56.1629, 10.2039),  # Aarhus city centre
    dist=5000,            # 5km radius
    network_type="walk"
)

print(f"✅ Done!")
print(f"Number of streets: {graph.number_of_edges()}")
print(f"Number of intersections: {graph.number_of_nodes()}")

# Save it so we don't need to download it again
ox.save_graphml(graph, "output/aarhus_walk.graphml")
print("✅ Saved as aarhus_walk.graphml")

import matplotlib.pyplot as plt

print("Plotting street network...")
fig, ax = ox.plot_graph(
    graph,
    figsize=(12, 10),
    node_size=0,
    edge_linewidth=0.5,
    edge_color="steelblue",
    bgcolor="white",
    show=False
)
plt.title("Aarhus Walking Network")
plt.savefig("output/aarhus_streets.png", dpi=150, bbox_inches="tight")
print("✅ Saved as aarhus_streets.png")
plt.show()
print(f"Number of streets: {graph.number_of_edges()}")
print(f"Number of intersections: {graph.number_of_nodes()}")