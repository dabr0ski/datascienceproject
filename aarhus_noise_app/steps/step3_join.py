import geopandas as gpd
import osmnx as ox

print("Loading saved data...")
noise = gpd.read_file("output/aarhus_noise.geojson")
graph = ox.load_graphml("output/aarhus_walk.graphml")

# Convert graph to street segments
print("Converting streets to dataframe...")
edges = ox.graph_to_gdfs(graph, nodes=False)
print(f"Street segments: {len(edges)}")

# Match coordinate systems
print("Matching coordinate systems...")
edges = edges.to_crs(noise.crs)

# Spatial join — match noise to streets
print("Joining noise to streets...")
edges_noise = gpd.sjoin(edges, noise[['isov1', 'geometry']],
                         how='left', predicate='intersects')

# Fill streets with no noise data with 50 dB (silent)
edges_noise['isov1'] = edges_noise['isov1'].fillna(50)

# Add noise category labels
def noise_category(db):
    if db <= 50:   return 'Silent'
    elif db <= 53: return 'Quiet'
    elif db <= 58: return 'Moderate'
    elif db <= 63: return 'Loud'
    elif db <= 68: return 'Very Loud'
    else:          return 'Extremely Loud'

edges_noise['noise_category'] = edges_noise['isov1'].apply(noise_category)

# Add exponential penalty weights
def noise_penalty(db):
    if db <= 50:   return 1
    elif db <= 53: return 2
    elif db <= 58: return 4
    elif db <= 63: return 8
    elif db <= 68: return 16
    else:          return 32

edges_noise['penalty'] = edges_noise['isov1'].apply(noise_penalty)

print("✅ Done!")
print(f"Noise levels on streets: {sorted(edges_noise['isov1'].unique())}")
print("\nNoise categories:")
print(edges_noise['noise_category'].value_counts())

# Save
edges_noise.to_file("output/aarhus_streets_noise.geojson", driver="GeoJSON")
print("✅ Saved as aarhus_streets_noise.geojson")