import folium
import pandas

# Load in our volcano data.
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
elev = list(data["ELEV"])

our_map = folium.Map(location=[40.0, -110.0], zoom_start=5, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")

html = """<h4>Volcano information:</h4>
<div>Name: %s</div>
<div>Height: %s m</div>
"""


def color_picker(elevation):
    if elevation < 1000:
        return "lightblue"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

# Add volcano data to the map
for lt, ln, nm, el in zip(lat, lon, name, elev):
    iframe = folium.IFrame(html=html % (nm, str(el)), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe),
                                      fill_color=color_picker(el), fill=True, fill_opacity=0.8, color="black"))

# Population map data
fgp = folium.FeatureGroup(name="Population")
geo_data = open("world.json", "r", encoding="utf-8-sig")
fgp.add_child(folium.GeoJson(data=geo_data.read(),
                             style_function=lambda x: {"fillColor": "green" if x["properties"]["POP2005"] < 10000000
                             else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))
geo_data.close()

our_map.add_child(fgv)
our_map.add_child(fgp)
our_map.add_child(folium.LayerControl())
our_map.save("map.html")
