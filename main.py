import json
import googlemaps 
import datetime
import time
from argparse import ArgumentParser
import os
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
def setup():
    parser = ArgumentParser()
    parser.add_argument('--api_key')
    args = parser.parse_args()
    if os.path.exists('credentials.json'): 
            with open('credentials.json') as f:
                data = json.load(f)
            api_key = data['MAPS_API_KEY']
    else:
        api_key = args.api_key
    gmaps = googlemaps.Client(key=api_key)
    return gmaps
def compute_itinerary(gmaps):
    # check first if credentials file is available
    origin_location = "Schaeracher 2 8053 Zuerich Switzerland"
    directions_to_eth = gmaps.directions(origin_location, "ETH Zurich", mode="transit", departure_time=datetime.datetime.now())
    # write directions to file correclty formatted
    with open('directions_to_eth.json', 'w') as outfile:
        json.dump(directions_to_eth, outfile, indent=4, sort_keys=True)

def get_times(gmaps):
    compute_itinerary(gmaps)
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
    if now.hour < 20 and now.hour > 7:
        if now.minute < 30:
            return 30 - now.minute
        else:
            return 60 - now.minute
    else:
        return 1000000000000

gmaps=setup()
window = tk.Tk()
# window.attributes('-zoomed', True)
window.geometry("500x350")
window.configure(background='white')

window.title(str(datetime.datetime.now()))

image = Image.open("31logo.png")  # Replace with the path to your image file
image = image.resize((120, 100))  # Resize the image as needed
image = ImageTk.PhotoImage(image)
image_label = tk.Label(window, image=image)

image91 = Image.open("91logo.png")  # Replace with the path to your image file
image91 = image91.resize((120, 100))  # Resize the image as needed
image91 = ImageTk.PhotoImage(image91)
image_label_91 = tk.Label(window, image=image91)

custom_font = font.Font(family="Helvetica", size=36)
# minutes_until_next_31 = datetime.datetime.now().minute
text_label_31 = tk.Label(window, text=str(get_times(gmaps)), font=custom_font, fg="blue", bg="white")
text_label_91 = tk.Label(window, text=str(time_until_next_91())+ " min", font=custom_font, fg="blue", bg="white")

# Use the grid() method to position the widgets
image_label.grid(row=0, column=0, padx=30, pady=10)
text_label_31.grid(row=0, column=1, padx=100)
image_label_91.grid(row=1, column=0, padx=30, pady=100)
text_label_91.grid(row=1, column=1, padx=100, pady=100)
def update_text():
    if datetime.datetime.now().hour > 0 and datetime.datetime.now().hour < 7:
        text_label_31.config(text="No buses at night")
        text_label_91.config(text="No buses at night")
        window.after(60000, update_text)
        return
    text_label_31.config(text=str(get_times(gmaps)))
    text_label_91.config(text=str(time_until_next_91())+ " min")
    window.after(60000, update_text)







update_text()
window.mainloop()
