"""This file implements a GUI that allows users to find nearby food banks.

It is able to use various ways such as the person's IP address or a manual
entry to find nearby search results in food banks.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import googlemaps
from geopy.geocoders import Nominatim
import geocoder
from geopy.distance import geodesic
import webbrowser
import urllib.parse

API_KEY = ""

food_bank_links = {}

class FoodBankLocatorGUI:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        label_location = ttk.Label(self.parent, text="Location:")
        label_location.grid(row=0, column=0, padx=5, pady=5)
        entry_location = ttk.Entry(self.parent, width=30)
        entry_location.grid(row=0, column=1, padx=5, pady=5)

        label_radius = ttk.Label(self.parent, text="Radius:")
        label_radius.grid(row=1, column=0, padx=5, pady=5)
        entry_radius = ttk.Entry(self.parent, width=10)
        entry_radius.grid(row=1, column=1, padx=5, pady=5)

        radius_options = [1, 2.5, 5, 7.5, 10]


        def autogenerate_location():
            """Obtain the user's location based on their IP address."""
            try:
                location = geocoder.ip('me')
                if location.ok:
                    address = location.address
                    entry_location.delete(0, tk.END)
                    entry_location.insert(tk.END, address)
                else:
                    messagebox.showerror("Error", "Unable to find the user's location. "
                                        "Please enter it manually.")
            except geocoder.GeocoderTimedOut:
                messagebox.showerror("Error", "Geocoding service timed out. "
                                    "Please try again later.")
            except geocoder.GeocoderUnavailable:
                messagebox.showerror("Error", "Geocoding service is currently unavailable. "
                                    "Please try again later.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to autogenerate location: {str(e)}")


        btn_autogenerate_location = ttk.Button(self.parent, text="Autogenerate Location",
                                            command=autogenerate_location)
        btn_autogenerate_location.grid(row=0, column=2, padx=5, pady=5)


        def handle_preselected_radius_selection(event):
            """Handles the selection of a preselected radius.

            Args:
                event (Event): The event information
            """
            selected_radius = combo_preselected_radius.get()
            entry_radius.delete(0, tk.END)
            entry_radius.insert(tk.END, selected_radius)


        combo_preselected_radius = ttk.Combobox(self.parent, values=radius_options,
                                                state="readonly", width=10)
        combo_preselected_radius.grid(row=2, column=1, padx=5, pady=5)
        combo_preselected_radius.set(radius_options[2])
        combo_preselected_radius.bind("<<ComboboxSelected>>", handle_preselected_radius_selection)

        label_radius_unit = ttk.Label(self.parent, text="Unit:")
        label_radius_unit.grid(row=1, column=2, padx=5, pady=5)
        radius_unit = tk.StringVar(value="Miles")
        combo_radius_unit = ttk.Combobox(self.parent, textvariable=radius_unit,
                                        state="readonly", width=10)
        combo_radius_unit.grid(row=1, column=3, padx=5, pady=5)
        combo_radius_unit['values'] = ("Miles", "Kilometers")

        btn_search = ttk.Button(self.parent, text="Search Food Banks",
                                command=lambda: get_nearby_food_banks(radius_unit.get()))
        btn_search.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

        label_food_banks = ttk.Label(self.parent, text="Food Banks:")
        label_food_banks.grid(row=4, column=0, padx=5, pady=5)
        listbox_food_banks = tk.Listbox(self.parent, width=40)
        listbox_food_banks.grid(row=5, column=0, columnspan=4, padx=5, pady=5)


        def geocode_address(address):
            """Geocodes the given address and returns the latitude and longitude.

            Args:
                address (str): The user's address

            Returns:
                tuple: A tuple containing latitude and longitude of the address
            """
            geolocator = Nominatim(user_agent="food_bank_locator")
            location = geolocator.geocode(address)
            return (location.latitude, location.longitude) if location else None


        def calculate_distance(location1, location2):
            """Calculates the distance between two locations using lat. & long.

            Args:
                location1 (tuple): A tuple containing latitude and longitude of the first location
                location2 (tuple): A tuple containing latitude and longitude of the second location

            Returns:
                float: The distance between two locations in miles
            """
            return round(geodesic(location1, location2).miles, 2)


        def find_closest_food_bank(geocoded_location):
            """Finds the closest food bank to the given geocoded location.

            Args:
                geocoded_location (tuple): A tuple containing latitude and longitude of the location

            Returns:
                tuple: A tuple containing latitude and longitude of the closest food bank
            """
            gmaps = googlemaps.Client(key=API_KEY)
            response = gmaps.places_nearby(
                location=geocoded_location,
                keyword="food bank",
                rank_by="distance",
                type="food",
            )
            food_banks = response["results"]
            return (food_banks[0]["geometry"]["location"]["lat"],
                    food_banks[0]["geometry"]["location"]["lng"]) if food_banks else None


        def get_nearby_food_banks(radius_unit):
            """Gets the nearby food banks based on the location and search radius.

            Args:
                radius_unit (str): The unit of the search radius ("Miles" or "Kilometers").
            """
            location = entry_location.get()
            if not location:
                messagebox.showerror("Error", "Please enter your location.")
                return

            radius_value = entry_radius.get()
            if not radius_value:
                messagebox.showerror("Error", "Please enter a search radius.")
                return

            radius = float(radius_value)
            if radius_unit == "Miles":
                radius *= 1609.34
            elif radius_unit == "Kilometers":
                radius *= 1000

            geocoded_location = geocode_address(location)
            if not geocoded_location:
                messagebox.showerror("Error", "Failed to geocode the entered address.")
                return

            gmaps = googlemaps.Client(key=API_KEY)

            try:
                response = gmaps.places_nearby(
                    location=geocoded_location,
                    keyword="food bank",
                    radius=radius,
                    type="food",
                )

                food_banks = response["results"]

                listbox_food_banks.delete(0, tk.END)

                for bank in food_banks:
                    name = bank['name']
                    address = bank['vicinity']
                    map_link = ("https://www.google.com/maps/search/?api=1&query="
                                + f"{urllib.parse.quote(name)}"
                                + f"{urllib.parse.quote(address)}")
                    listbox_food_banks.insert(tk.END, name)
                    food_bank_links[name] = map_link

                if len(food_banks) > 0:
                    messagebox.showinfo("Food Banks",
                                        f"Found {len(food_banks)} food banks nearby.")
                else:
                    closest_food_bank = find_closest_food_bank(geocoded_location)
                    if closest_food_bank:
                        distance = calculate_distance(geocoded_location,
                                                    closest_food_bank)

                        messagebox.showinfo("Food Banks", f"No food banks found nearby. "
                                            "The closest food bank is approximately in "
                                            f"{distance} {radius_unit}.")
                        closest_radius_option = min(radius_options,
                                                    key=lambda x: abs(x - distance))
                        combo_preselected_radius.set(closest_radius_option)
                        entry_radius.delete(0, tk.END)
                        entry_radius.insert(tk.END, closest_radius_option)
                    else:
                        messagebox.showinfo("Food Banks", "No food banks found nearby.")
            except googlemaps.exceptions.ApiError:
                messagebox.showerror("Error",
                                    "An error occurred while retrieving food banks.")


        def open_selected_food_bank(event):
            """Opens the Google Maps link for the selected food bank.

            Args:
                event (Event): The event information
            """
            selected_bank = listbox_food_banks.get(listbox_food_banks.curselection())
            map_link = food_bank_links[selected_bank]
            webbrowser.open(map_link)


        listbox_food_banks.bind("<Double-Button-1>", open_selected_food_bank)
