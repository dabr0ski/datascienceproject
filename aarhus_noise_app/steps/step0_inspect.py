import geopandas as gpd

print("Loading noise data...")
noise = gpd.read_file("data/dk_2022_vej_1_5m.tab")

print("\n--- BASIC INFO ---")
print("Number of noise zones:", len(noise))
print("Columns:", noise.columns.tolist())
print("Coordinate system:", noise.crs)
print("Data types:\n", noise.dtypes)

print("\n--- NOISE LEVELS ---")
print("Unique noise levels (isov1):", sorted(noise['isov1'].unique()))
print("Unique noise levels (isov2):", sorted(noise['isov2'].unique()))

print("\n--- STATISTICS ---")
print(noise[['isov1', 'isov2', 'shape_leng', 'shape_area']].describe())

print("\n--- FIRST 5 ROWS ---")
print(noise.head())

print("\n--- GEOGRAPHIC EXTENT ---")
print("Total bounds:", noise.total_bounds)