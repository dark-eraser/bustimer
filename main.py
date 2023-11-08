import json
import googlemaps 
import datetime
import time
from argparse import ArgumentParser
import os
import tkinter as tk
from tkinter import font




def compute_itinerary(api_key_arg=""):
    # check first if credentials file is available
    if os.path.exists('credentials.json'): 
        with open('credentials.json') as f:
            data = json.load(f)
        api_key = data['MAPS_API_KEY']
    else:
        api_key = api_key_arg
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
                    # print(f"Bus {bus_number} departs at {departure_time}")
                    return departure_time
        else:
            print("Steps not found in the first leg.")
    else:
        print("Legs not found in the response.")
    print("No bus found.")
def time_until_next_91():
    now = datetime.datetime.now()
    if now.minute < 30:
        return 30 - now.minute
    else:
        return 60 - now.minute


window = tk.Tk()
window.geometry("400x200")
window.title("Time until next 31")

custom_font = font.Font(family="Helvetica", size=16)
text_label_31 = tk.Label(window, text="Next 31 is at: "+str(get_times()),font=custom_font,fg="blue")
text_label_31.pack(pady=20)
text_label_91 = tk.Label(window, text="Next 91 bus is in: "+str(time_until_next_91())+" minutes.",font=custom_font,fg="blue")
text_label_91.pack(pady=20)
def update_text():
    compute_itinerary(args.api_key)
    text_label_31.config(text="Next 31 is at: "+str(get_times()))
    text_label_91.config(text="Next 91 bus is in: "+str(time_until_next_91())+" minutes.")
    window.after(60000, update_text)


parser = ArgumentParser()
parser.add_argument('--api_key')
args = parser.parse_args()




update_text()
window.mainloop()
