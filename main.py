import json
import googlemaps 
import datetime
import time
from argparse import ArgumentParser

def compute_itinerary(api_key=""):
  with open('credentials.json') as f:
      data = json.load(f)
  if data['MAPS_API_KEY']:
    api_key = data['MAPS_API_KEY']
  print(api_key)
  gmaps = googlemaps.Client(key=api_key)
  origin_location = "9H4X+R6 Zürich"
  directions_to_eth = gmaps.directions(origin_location, "ETH Zurich", mode="transit", departure_time=datetime.datetime.now())
  # write directions to file correclty formatted
  with open('directions_to_eth.json', 'w') as outfile:
      json.dump(directions_to_eth, outfile, indent=4, sort_keys=True)

def get_times():
  with open('directions_to_eth.json') as f:
      data = json.load(f)
  legs = data[0]['legs']
  if legs and len(legs) > 0:
      leg = legs[0]
      if leg['steps'] and len(leg['steps']) > 0:
          for step in leg['steps']:
              if step['travel_mode'] == 'TRANSIT':
                  departure_time = step['transit_details']['departure_time']['text']
                  bus_number = step['transit_details']['line']['short_name']
                  print(f"Bus {bus_number} departs at {departure_time}")
      else:
          print("Steps not found in the first leg.")
  else:
      print("Legs not found in the response.")

def main():
    parser = ArgumentParser()
    parser.add_argument('api_key', help='Google Maps API key')
    args = parser.parse_args()
# run this every minute
    while True:
        compute_itinerary(args.api_key)
        get_times()
        time.sleep(60)

if __name__ == "__main__":
    main()