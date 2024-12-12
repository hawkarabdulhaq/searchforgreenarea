import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon

# Set up the title of the app
st.title("Green Area Polygons Viewer")

# Path to the GeoJSON file
geojson_file_path = "./data/Green_Area_Polygons.geojson"

# Load the GeoJSON file using GeoPandas
try:
    green_areas = gpd.read_file(geojson_file_path)

    # Ensure the CRS is set to a metric system for area calculations
    if green_areas.crs is None or not green_areas.crs.is_projected:
        green_areas = green_areas.to_crs(green_areas.crs or "EPSG:4326")  # Preserve original CRS or set default

    green_areas["area_m2"] = green_areas.geometry.to_crs("EPSG:3395").area  # Calculate area in square meters using Mercator projection
    green_areas["area_hectares"] = green_areas["area_m2"] / 10000  # Convert area to hectares
    st.success("GeoJSON file loaded successfully!")
except Exception as e:
    st.error(f"Error loading GeoJSON file: {e}")
    st.stop()

# Debug: Display the range of polygon areas
if not green_areas.empty:
    min_area_m2 = green_areas["area_m2"].min()
    max_area_m2 = green_areas["area_m2"].max()
    min_area_ha = green_areas["area_hectares"].min()
    max_area_ha = green_areas["area_hectares"].max()

    st.subheader("Debug Information: Area Ranges")
    st.write(f"Minimum Area: {min_area_m2:.2f} m² ({min_area_ha:.2f} hectares)")
    st.write(f"Maximum Area: {max_area_m2:.2f} m² ({max_area_ha:.2f} hectares)")

# Display the GeoJSON properties
if not green_areas.empty:
    st.subheader("GeoJSON File Properties")
    st.write(green_areas.head())

    # Add a search filter for polygon area
    st.subheader("Search Green Areas by Size")
    min_area = st.slider("Minimum Area (hectares):", 0.0, green_areas["area_hectares"].max(), 0.0, 0.1)
    max_area = st.slider("Maximum Area (hectares):", 0.0, green_areas["area_hectares"].max(), green_areas["area_hectares"].max(), 0.1)

    filtered_areas = green_areas[(green_areas["area_hectares"] >= min_area) & (green_areas["area_hectares"] <= max_area)]

    if filtered_areas.empty:
        st.warning("No polygons found within the specified area range.")
    else:
        st.write(f"Found {len(filtered_areas)} polygons within the specified range.")
        st.write(filtered_areas)

        # Set up the map
        m = folium.Map(location=[filtered_areas.geometry.centroid.y.mean(), filtered_areas.geometry.centroid.x.mean()],
                       zoom_start=12)

        # Add filtered GeoJSON to the map
        folium.GeoJson(filtered_areas, name="Filtered Green Areas").add_to(m)

        # Add Layer Control
        folium.LayerControl().add_to(m)

        # Display the map in Streamlit
        st_folium(m, width=700, height=500)
else:
    st.warning("The GeoJSON file is empty or contains no valid geometry.")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit")
