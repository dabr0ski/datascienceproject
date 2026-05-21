import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Loading noise data...")
noise = gpd.read_file("data/dk_2022_vej_1_5m.tab")
print(f"Loaded {len(noise)} zones")

# Convert coordinate system
noise_web = noise.to_crs(epsg=3857)

# Filter to Aarhus
aarhus = noise_web.cx[1115893:1155893, 7570913:7610913]
print(f"Aarhus zones: {len(aarhus)}")

# Save for later steps
aarhus.to_file("output/aarhus_noise.geojson", driver="GeoJSON")
print("✅ Saved aarhus_noise.geojson")

# Plot
fig, ax = plt.subplots(figsize=(12, 10))
aarhus.plot(column='isov1', cmap='RdYlGn_r', legend=True, alpha=0.6, ax=ax)
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=13)
plt.title("Aarhus Road Noise 2022 (dB)")
plt.savefig("output/aarhus_noise_map.png", dpi=150, bbox_inches="tight")
print("✅ Map saved!")
plt.show()
