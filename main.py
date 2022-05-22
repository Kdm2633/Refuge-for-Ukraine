import pandas as pd
import geopandas as gpd
import folium
from flask import Flask, render_template

app = Flask('app')


@app.route('/')
def map():
    return render_template('visualization.html')


@app.route('/howtohelp')
def howtohelp():
    return render_template('howtohelp.html')


# @app.route('/')
# def homepage():
#     return render_template('index.html')

# Refugee Data
refugee_data = pd.read_csv('data/UkraineRefugees.csv')
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

refugee_data = world.merge(refugee_data,
                           how='left',
                           left_on=['name'],
                           right_on=['Name'])
cols = refugee_data.columns[6:]
refugee_data = refugee_data.dropna(subset=cols, how='all')
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 200)
# print(world)
# print(refugee_data)

#ploting bubbles on map
#Arrays of country coordinates
long = [
    21.01178, 19.040236, 28.468344, 19.48489, 25.005936, 37.618423, 28.054094
]
latitude = [
    52.22977, 47.497913, 47.203705, 48.707485, 45.83774, 55.751244, 53.543472
]

# # Healthcare Facilities Data
healthcare_data = pd.read_csv('data/health_facilities.csv')
# print(healthcare_data["Region"])
ukr_geo = gpd.read_file(
    'data/ukraine_regions.json')  #administrative divisions shapefile
# healthcare_data = ukr_geo.merge(healthcare_data,
#                                 how='left',
#                                 left_on=['name_1'],
#                                 right_on=['Region'])

healthcare_data = healthcare_data.dropna()
# print(ukr_geo['name_1'])
#print(healthcare_data)

# Mapping
m = folium.Map(
    location=[50.715, 24.213],
    zoom_start=4,
    min_zoom=4,
    max_zoom=7,
    tiles=
    "https://api.mapbox.com/styles/v1/lumii/cl3g4e55100aq14qumgn4whkg/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibHVtaWkiLCJhIjoiY2wzZzN3ZGEyMDVnZjNmcDc3Z3Jodm0wbyJ9.oTc222D0JZekjMQD_1EGYw",
    attr="mapbox")
folium.GeoJson(data=ukr_geo["geometry"]).add_to(m)


def plot_circles():
    for x in range(0, len(refugee_data["Name"])):
        folium.CircleMarker(location=[latitude[x], long[x]],
                            radius=50,
                            color="blue",
                            fill_color="blue").add_to(m)


plot_circles()

custom_scale = (healthcare_data['Health_Facilities'].quantile(
    (0, 0.2, 0.4, 0.6, 0.8, 1))).tolist()


folium.Choropleth(
    geo_data=ukr_geo,
    name="Healthcare Facilities",
    data=healthcare_data,
    columns=["Region", "Health_Facilities"],
    key_on="feature.properties.name_1",
    threshold_scale=custom_scale,
    fill_color="YlGn",
    fill_opacity=0.7,
    nan_fill_color="White",
    line_opacity=.1,
    legend_name="Number of Healthcare Facilities in Each Province",
).add_to(m)

healthcare_geo = ukr_geo.merge(healthcare_data,
                                how='left',
                                left_on=['name_1'],
                                right_on=['Region'])

folium.features.GeoJson(healthcare_geo,
                        name='Labels',
                        style_function=lambda x: {
                            'color': 'transparent',
                            'fillColor': 'transparent',
                            'weight': 0
                        },
                        tooltip=folium.features.GeoJsonTooltip(
                            fields=['name_1', 'Health_Facilities'],
                            aliases=['Province', 'Healthcare Facilities'],
                            labels=True,
                            sticky=False)).add_to(m)
folium.LayerControl().add_to(m)
m.save('./templates/maps.html')

app.run(host='0.0.0.0', port=8080, debug=True)
