import matplotlib as mpl
import folium
import csv
import pandas as pd

csvFile = open("D:/sort_by_term/2.5/algorithm_class/project/data/chengdu_50_1.csv", "r")

dict_reader = csv.DictReader(csvFile)
cdata=pd.DataFrame(dict_reader).astype(float)

cd_map = folium.Map(location = [30.7,104], zoom_start=11.5)

# Instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# Loop through the 200 crimes and add each to the incidents feature group
for lat, lng, num in zip(cdata.LonDrop, cdata.LatDrop, cdata.NumOrder):
    incidents.add_child(
        folium.Marker(
            location = [lng, lat],
            popup=num,
            icon=folium.Icon(color='red', icon="bus", prefix="fa")
        )
    )
    
# starting point
incidents.add_child(
    folium.Marker(
        location = [30.641199999999998, 104.04945333333333],
        icon=folium.Icon(color='blue', icon="bus", prefix="fa")
    )
)

# Add incidents to map
cd_map.add_child(incidents)
# help(folium.Icon)
cd_map.save('alg_proj/map_chengdu.html')
    
cd_map