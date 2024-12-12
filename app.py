import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Set up the title of the app
st.title("Green Area Polygons Viewer")

# Path to the GeoJSON file
geojson_file_path = "./data/Green_Area_Polygons.geojson"

# Load the GeoJSON file using GeoPandas
try:
    green_areas = gpd.read_file(geojson_file_path)
    st.success("GeoJSON file loaded successfully!")
except Exception as e:
    st.error(f"Error loading GeoJSON file: {e}")
    st.stop()

# Display the GeoJSON properties
if not green_areas.empty:
    st.subheader("GeoJSON File Properties")
    st.write(green_areas.head())

    # Set up the map
    m = folium.Map(location=[green_areas.geometry.centroid.y.mean(), green_areas.geometry.centroid.x.mean()],
                   zoom_start=12)

    # Add GeoJSON to the map
    folium.GeoJson(green_areas, name="Green Areas").add_to(m)

    # Add Layer Control
    folium.LayerControl().add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700, height=500)
else:
    st.warning("The GeoJSON file is empty or contains no valid geometry.")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit")
