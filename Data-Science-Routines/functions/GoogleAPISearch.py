
import googlemaps
import pandas
import json

gmaps = googlemaps.Client(key='AIzaSyAaep210hhXznobsOZGN5jMuEb8UNrW6gI')

# Geocoding an address
df=pandas.read_csv("C:\\Users\\Felipe Torres\\Desktop\\TheBigHackathon\\datasets\\CNES.csv", sep=";", encoding="UTF-8")

for index, row in df.iterrows():
    try:
        geocode_result = gmaps.geocode(row["Padronizado"])
        if not geocode_result:
            continue
        print(str(row["CNES"]) + ";" + str(json.dumps(geocode_result)))
    except():
        print()

