import folium
import csv

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from folium.plugins import Geocoder
from geopy.distance import great_circle

# Create a map object with an initial location (latitude and longitude)
m = folium.Map(location=[29.1899, -81.0488], zoom_start=10)  # ERAU coordinates
Geocoder().add_to(m)

# Create a feature group for each category of markers
lightblue_markers = folium.FeatureGroup(name='Statutory Rape') # Light Blue Markers
red_markers = folium.FeatureGroup(name='Sexual Battery') # Red Markers
pink_markers = folium.FeatureGroup(name='Lewd and Lascivious Conduct') # Pink Markers
lightgreen_markers = folium.FeatureGroup(name='Posession of Inappropriate Photos/Videos of Minors') # Light Green Markers
darkblue_markers = folium.FeatureGroup(name='Sexual Predator or Unknown') # Dark Blue Markers                           
                                     
# Define custom icon colors and properties
icon_lightblue = folium.Icon(color='lightgreen', icon='cloud')
icon_red = folium.Icon(color='red', icon='star')
icon_pink = folium.Icon(color='pink')
icon_lightgreen = folium.Icon(color='lightgreen')
icon_darkblue = folium.Icon(color='darkblue')

# Add landmark markers to the map with custom icons
erau_coords = (29.1899, -81.0488)
folium.Marker(erau_coords, tooltip='Embry-Riddle Aeronautical University', icon=icon_lightblue).add_to(m)

# Function to add apartment markers to the map
def add_apartment_markers():
    with open('csv/ApartmentDatabase.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            complex_name = row['\ufeffcomplex'] # Remove BOM character from excel to csv conversion encoding
            address = row['address']
            latitude = float(row['lat'])
            longitude = float(row['long'])
            folium.Marker(
                location=[latitude, longitude],
                popup=f"{complex_name}<br>{address}",
                icon=folium.Icon(color='blue', icon='home')
            ).add_to(m)

# Call the function to add apartment markers
add_apartment_markers()

# Function to add house markers to the map
def add_house_markers():
    with open('csv/HomeDatabase.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            address = row['\ufeffaddress'] # Remove BOM character from excel to csv conversion encoding
            latitude = float(row['lat'])
            longitude = float(row['long'])
            folium.Marker(
                location=[latitude, longitude],
                popup=f"{address}",
                icon=folium.Icon(color='green', icon='home')
            ).add_to(m)

# Call the function to add house markers
add_house_markers()

# Function to add sex offender markers to the map
def add_sex_offender_markers():
    with open('csv/SexualOffenderDatabase.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['\ufeffname'] # Remove BOM character from excel to csv conversion encoding
            address = row['address']
            latitude = float(row['lat'])
            longitude = float(row['long'])
            crime = row['crime']

            # Assigning marker color based on crime
            if crime == 'LEWD OR LASCIVIOUS CONDUCT':
                icon_color = 'pink'
                marker_group = pink_markers
            elif crime == 'Sexual Battery':
                icon_color = 'red'
                marker_group = red_markers
            elif crime == 'Poss Of Photo/picture Showing Sexual Performance by a child':
                icon_color = 'lightgreen'
                marker_group = lightgreen_markers
            else:  # Default case for 'Sexual Predator or Unknown'
                icon_color = 'darkblue'
                marker_group = darkblue_markers

            # Creating the marker
            folium.Marker(
                location=[latitude, longitude],
                popup=f"{name}<br>{address}",
                icon=folium.Icon(color=icon_color)
            ).add_to(marker_group)

# Call the function to add sex offender markers
add_sex_offender_markers()

# Define a custom search bar using HTML and JavaScript
search_html = """
<div style="position: fixed; 
            top: 10px; right: 10px; 
            background-color: white; padding: 10px; z-index: 9999;">
  <input id="search" type="text" placeholder="Enter address" oninput="initAutocomplete()">
</div>
<script>

map</script>
"""

# Define a custom legend using HTML
legend_html = """
<div style="position: fixed; 
            bottom: 50px; left: 50px; 
            border: 2px solid grey; z-index: 9999; 
            background-color: white; padding: 10px;">
  <strong>Legend</strong><br>
  <i class="fa fa-map-marker fa-2x" style="color: lightblue"></i> Statutory Rape<br>
  <i class="fa fa-map-marker fa-2x" style="color: red"></i> Sexual Battery<br>
  <i class="fa fa-map-marker fa-2x" style="color: pink"></i> Lewd and Lascivious Conduct<br>
  <i class="fa fa-map-marker fa-2x" style="color: lightgreen"></i> Posession of inappropriate photos/videos of minors<br>
  <i class="fa fa-map-marker fa-2x" style="color: darkblue"></i> Sexual Predator or Unknown
</div>
"""
# Define custom JavaScript code for radius selection
radius_selection_js = """
function onSearchResult(e) {
    var radiusOptions = [1, 3, 5];
    var radiusSelect = document.createElement('select');
    radiusSelect.id = 'radiusSelect';
    
    for (var i = 0; i < radiusOptions.length; i++) {
        var option = document.createElement('option');
        option.value = radiusOptions[i];
        option.text = radiusOptions[i] + ' miles';
        radiusSelect.appendChild(option);
    }
    
    radiusSelect.addEventListener('change', function() {
        var selectedRadius = this.value;
        alert('Selected Radius: ' + selectedRadius + ' miles');
    });
    
    var searchControl = document.querySelector('.leaflet-control-search');
    searchControl.appendChild(radiusSelect);
}

document.querySelector('.leaflet-control-search').addEventListener('search:locationfound', onSearchResult);
"""

# Add the custom search bar and legend to the map
#m.get_root().html.add_child(folium.Element(search_html))
m.get_root().html.add_child(folium.Element(legend_html))

# Add the feature groups to the map
m.add_child(lightblue_markers)
m.add_child(red_markers)
m.add_child(pink_markers)
m.add_child(lightgreen_markers)
m.add_child(darkblue_markers)

# Add a layer control to toggle markers
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('safe-housing-map.html')
