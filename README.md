# Quiet Routes Aarhus

A noise-aware pedestrian routing application for Aarhus, Denmark. The app calculates both the fastest route and the quietest route between two locations, helping users avoid noisy streets based on official Danish noise mapping data.

## Before running the scripts, create two empty folders in the project root:

    mkdir data
    mkdir output

Then download the noise data from the link below and place the files inside the data/ folder.
## Data

The noise data files are too large to include in this repository (approx. 200 MB). Download them from Google Drive and place them in the data/ folder:

(https://drive.google.com/drive/folders/1NsxWhZL8yJWij34SbbLHwhi-DcI3IAVr?usp=share_link)

Replace the entire data/ folder with the downloaded files before running the scripts.

## Requirements

Python 3.9 or higher is required. Install all dependencies with:

    pip3 install geopandas osmnx networkx folium contextily matplotlib pandas geopy

## How to Run

Run the steps in order from the project root folder:

    python3 steps/step0_inspect.py
    python3 steps/step1_load.py
    python3 steps/step2_streets.py
    python3 steps/step3_join.py
    python3 steps/step4_routing.py

After running step 4, the file output/route_map.html will open automatically in your browser showing both routes.If not opening please open the file from the output folder.

## Changing the Start and End Location

To change the route, open steps/step4_routing.py and edit lines 53 and 54:

    start = (56.1572, 10.2107)  # latitude, longitude of start point
    end   = (56.1711, 10.1952)  # latitude, longitude of end point

Replace the coordinates with any location in Aarhus. Coordinates must be in decimal format (latitude, longitude).

To find coordinates for any address in Aarhus, go to OpenStreetMap, search for the address, right-click on the location and the coordinates will appear in the URL in the format: latitude, longitude.

    https://www.openstreetmap.org

## Project Structure

    aarhus_noise_app/
    |-- data/                            # Download from Google Drive link above
    |-- output/                          # Generated files saved here
    |-- steps/
    |   |-- step0_inspect.py            # Inspect raw data
    |   |-- step1_load.py               # Load and visualise noise data
    |   |-- step2_streets.py            # Download street network
    |   |-- step3_join.py               # Join noise data to streets
    |   |-- step4_routing.py            # Calculate and display routes
    |-- README.md

## How It Works

The routing algorithm uses Dijkstra's shortest path algorithm with a noise-weighted cost function. Each street segment is assigned a penalty weight based on its noise level, derived from WHO Environmental Noise Guidelines (2018). Streets with higher noise levels receive higher penalty weights, making them more costly to traverse and naturally guiding the algorithm towards quieter alternatives.

Penalty weights are calculated as the ratio of human annoyance at each noise level relative to the silent baseline, based on WHO Table 10 data on the association between road traffic noise and percentage of highly annoyed respondents.

## Data Sources

- Noise data: Miljøstyrelsen (Danish Environmental Protection Agency), 2022
- Street network: OpenStreetMap via OSMnx
- Noise thresholds: WHO Environmental Noise Guidelines for the European Region, 2018
- Collected under EU Directive 2002/49/EC on environmental noise assessment

## References

WHO. (2018). Environmental Noise Guidelines for the European Region.
https://www.who.int/europe/publications/i/item/9789289053563

Wang et al. (2020). Quiet Route Planning for Pedestrians in Traffic Noise Polluted Environments.
IEEE Transactions on Intelligent Transportation Systems.
https://doi.org/10.1109/tits.2020.3004660

Boeing, G. (2017). OSMnx. Computers, Environment and Urban Systems, 65, 126-139.
https://doi.org/10.1016/j.compenvurbsys.2017.05.004

Miljøstyrelsen. (2022). Noise mapping and action plans.
https://eng.mst.dk/industry/noise/noise-mapping-and-action-plans
