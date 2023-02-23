import requests
from datetime import datetime
import folium
import webbrowser
import os
import time
'''
Usage requires:

pip install requests
pip install folium

api key from https://api.nasa.gov/ to replace DEMO_KEY

Demo Key will work but limited to 30 requests an hour
'''

def draw_circle_on_map(center_lat, center_lon, diameter_meters,label):
    
    #Making Map
    m = folium.Map(location=(center_lat, center_lon), tiles="cartodb positron",zoom_start=13)
    folium.Circle(location=[center_lat, center_lon], popup=label, fill_color='red', radius=diameter_meters, weight=2, color="black").add_to(m)

    #Adding Title
    title_html = '''
             <h3 align="center" style="font-size:16px"><b>Asteroid Name: {} , Diameter: {:.2f} meters</b></h3>
             '''.format(label,diameter_meters)   
    m.get_root().html.add_child(folium.Element(title_html))
    
    #Save and Show map
    m.save("asteroid.html")
    webbrowser.open("asteroid.html")
    

# Set up the API URL and parameters
url = "https://api.nasa.gov/neo/rest/v1/feed"
key = "DEMO_KEY"

today = datetime.today().strftime('%Y-%m-%d')
date = input("Input a date in the format YYYY-MM-DD Including the dashes (ex 2023-01-21). Leave blank for today:\n")
if date.upper() == "TODAY" or date =="":
    date = today

params = {"start_date": date, "end_date": date, "api_key": key}

# Fetch data from the API and convert it to JSON format
response = requests.get(url, params=params)
data = response.json()
# Extract the near-earth objects from the data
near_earth_objects = data["near_earth_objects"][date]
# list to store diameters and names by list #
diameters = []
names = []
# Print out some information about each near-earth object
print(f'\nAsteroids closest to earth on {date}:\n')
i= 1 #Number Label
for neo in near_earth_objects:
    #Get/Record Values
    name = neo["name"]
    min_diameter = neo["estimated_diameter"]["meters"]["estimated_diameter_min"]
    max_diameter = neo["estimated_diameter"]["meters"]["estimated_diameter_max"]
    rel_velocity =  neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]
    miss_distance =  neo["close_approach_data"][0]["miss_distance"]["astronomical"]
    danger = neo["is_potentially_hazardous_asteroid"]
    diameters.append(max_diameter)
    names.append("name")
    #Print everything out
    print(f"{i}. {name}: \n\t Diameter = {min_diameter:.2f}m - {max_diameter:.2f}m")
    print(f"\t Velocity = {float(rel_velocity):.2f} km/h")
    print(f"\t Miss Distance = {float(miss_distance):.2f} AU")
    print(f"\t Possibly Dangerous = {danger}")
    i+=1  #Number Label increase

#Visualize on map

toronto_coords  = [43.6532,-79.3832] #Latitude, Longitude

display_choice = input("Would you like to visualize an asteroid? y/n: \n")

if display_choice.upper() == "Y":

    display_choice = input("Which one? Input either its number in the list or max for biggest: \n")

    if display_choice.upper() == "MAX":
        index = diameters.index(max(diameters)) # the index of the biggest diameter
        draw_circle_on_map(toronto_coords[1], toronto_coords[0], max(diameters),names[index]) #The biggest asteroid name and size

    elif int(display_choice) <= len(diameters):
         index = display_choice
         draw_circle_on_map(toronto_cords[1], toronto_coords[0], diameters[index],names[index]) #The # asteroid and  size

#Remove file after giving 10s for it to open
time.sleep(10)
if os.path.exists("asteroid.html"):
        os.remove("asteroid.html")
else:
    print("The file does not exist") 