import osmnx as ox
import networkx as nx
import geopandas as gpd
import folium
import pickle

# Load data
print("Loading data...")
graph = ox.load_graphml("output/aarhus_walk.graphml")
edges_noise = gpd.read_file("output/aarhus_streets_noise.geojson")

# Noise penalty based on WHO thresholds — exponential scaling
def noise_penalty(db):
    if db <= 50:   return 1   # Silent
    elif db <= 55: return 1.28   # Quiet
    elif db <= 60: return 1.76   # Moderate
    elif db <= 65: return 2.43   # Loud
    elif db <= 70: return 3.3 # Very Loud
    elif db <= 75: return 5.64  # Very Loud
    else:          return 5.64  # Extremely Loud

# Build noise lookup
print("Reading noise levels...")
noise_lookup = {}
for _, row in edges_noise.iterrows():
    try:
        u = int(row['u'])
        v = int(row['v'])
        db = float(row['isov1'])
        noise_lookup[(u, v)] = noise_penalty(db)
    except:
        continue

# Build raw dB lookup for statistics
db_lookup = {}
for _, row in edges_noise.iterrows():
    try:
        u = int(row['u'])
        v = int(row['v'])
        db = float(row['isov1'])
        db_lookup[(u, v)] = db
    except:
        continue

# Apply cost to each street
print("Applying noise weights...")
for u, v, key, data in graph.edges(keys=True, data=True):
    length = data.get('length', 10)
    penalty = noise_lookup.get((u, v), noise_lookup.get((v, u), 1))
    data['quiet_cost'] = length * penalty

# Start and end points
start = (56.1629, 10.1750)  # Viborgvej - west of Ringgaden
end   = (56.1629, 10.2200)  # Nørrebrogade - east of Ringgaden

# Find nearest nodes
print("Finding routes...")
orig = ox.nearest_nodes(graph, start[1], start[0])
dest = ox.nearest_nodes(graph, end[1], end[0])

# Calculate both routes
fast_route  = nx.shortest_path(graph, orig, dest, weight='length')
quiet_route = nx.shortest_path(graph, orig, dest, weight='quiet_cost')

# Calculate distances
fast_length  = sum(graph[u][v][0].get('length', 0) for u, v in zip(fast_route[:-1],  fast_route[1:]))
quiet_length = sum(graph[u][v][0].get('length', 0) for u, v in zip(quiet_route[:-1], quiet_route[1:]))
detour_pct   = ((quiet_length / fast_length) - 1) * 100

# Calculate average noise
def avg_noise(route):
    levels = []
    for u, v in zip(route[:-1], route[1:]):
        db = db_lookup.get((u, v), db_lookup.get((v, u), 50))
        levels.append(db)
    return sum(levels) / len(levels)

fast_noise  = avg_noise(fast_route)
quiet_noise = avg_noise(quiet_route)

print(f"\n--- ROUTE COMPARISON ---")
print(f"Fast route:  {fast_length:.0f}m, avg noise: {fast_noise:.1f} dB")
print(f"Quiet route: {quiet_length:.0f}m, avg noise: {quiet_noise:.1f} dB")
print(f"Noise reduction: {fast_noise - quiet_noise:.1f} dB")
print(f"Distance increase: {detour_pct:.1f}%")

# Show on map
def route_to_coords(graph, route):
    return [(graph.nodes[n]['y'], graph.nodes[n]['x']) for n in route]

m = folium.Map(location=[56.1629, 10.2039], zoom_start=14)

folium.PolyLine(route_to_coords(graph, fast_route),
    color='red', weight=6,
    tooltip=f'Fastest: {fast_length:.0f}m | {fast_noise:.1f} dB').add_to(m)

folium.PolyLine(route_to_coords(graph, quiet_route),
    color='green', weight=6,
    tooltip=f'Quietest: {quiet_length:.0f}m | {quiet_noise:.1f} dB').add_to(m)

folium.Marker(route_to_coords(graph, quiet_route)[0],
    popup='Start', icon=folium.Icon(color='blue', icon='home')).add_to(m)
folium.Marker(route_to_coords(graph, quiet_route)[-1],
    popup='End', icon=folium.Icon(color='purple', icon='flag')).add_to(m)

m.save("output/route_map.html")
print("Map saved!")

import webbrowser
webbrowser.open("output/route_map.html")

with open("output/routes.pkl", "wb") as f:
    pickle.dump((graph, quiet_route, fast_route), f)
print("Routes saved!")