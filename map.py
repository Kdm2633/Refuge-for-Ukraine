import folium


# Mapping 
m = folium.Map(location=[50.715, 24.213], zoom_start=4, min_zoom=4, max_zoom=7,tiles="https://api.mapbox.com/styles/v1/lumii/cl3g4e55100aq14qumgn4whkg/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibHVtaWkiLCJhIjoiY2wzZzN3ZGEyMDVnZjNmcDc3Z3Jodm0wbyJ9.oTc222D0JZekjMQD_1EGYw", attr="mapbox")

# Creating Markers

folium.Marker(location=[50.000, 25.0000], icon=folium.Icon(color="blue"), draggable=True).add_to(m)

# Creating Markers
folium.CircleMarker(location=[50.000, 25.0000],
                    radius=50,
                    color="red",
                    fill_color="red").add_to(m)

m.save('./templates/maps.html')
