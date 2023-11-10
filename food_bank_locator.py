"""This module implements a graphical user interface that allows users 
to find nearby food banks and manage their food inventory."""

import tkinter as tk
from tkinter import ttk, messagebox
import googlemaps
from geopy.geocoders import Nominatim
import geocoder
from geopy.distance import geodesic
import webbrowser
import urllib.parse
import cv2
from pyzbar.pyzbar import decode
import requests

API_KEY = ""

food_bank_links = {}

window = tk.Tk()
window.title("Food Bank Locator and Inventory")
window.geometry("850x450")
window.resizable(True, True)

notebook = ttk.Notebook(window)
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
notebook.add(frame1, text='Food Bank Locator')
notebook.add(frame2, text='Food Inventory')
notebook.pack(expand=True, fill='both')

label_location = ttk.Label(frame1, text="Location:")
label_location.grid(row=0, column=0, padx=5, pady=5)
entry_location = ttk.Entry(frame1, width=30)
entry_location.grid(row=0, column=1, padx=5, pady=5)

label_radius = ttk.Label(frame1, text="Radius:")
label_radius.grid(row=1, column=0, padx=5, pady=5)
entry_radius = ttk.Entry(frame1, width=10)
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


btn_autogenerate_location = ttk.Button(frame1, text="Autogenerate Location",
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


combo_preselected_radius = ttk.Combobox(frame1, values=radius_options,
                                        state="readonly", width=10)
combo_preselected_radius.grid(row=2, column=1, padx=5, pady=5)
combo_preselected_radius.set(radius_options[2])
combo_preselected_radius.bind("<<ComboboxSelected>>", handle_preselected_radius_selection)

label_radius_unit = ttk.Label(frame1, text="Unit:")
label_radius_unit.grid(row=1, column=2, padx=5, pady=5)
radius_unit = tk.StringVar(value="Miles")
combo_radius_unit = ttk.Combobox(frame1, textvariable=radius_unit,
                                 state="readonly", width=10)
combo_radius_unit.grid(row=1, column=3, padx=5, pady=5)
combo_radius_unit['values'] = ("Miles", "Kilometers")

btn_search = ttk.Button(frame1, text="Search Food Banks",
                        command=lambda: get_nearby_food_banks(radius_unit.get()))
btn_search.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

label_food_banks = ttk.Label(frame1, text="Food Banks:")
label_food_banks.grid(row=4, column=0, padx=5, pady=5)
listbox_food_banks = tk.Listbox(frame1, width=40)
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

# Frame 2: Food Inventory

label_item = tk.Label(frame2, text="Food Item:")
label_item.grid(row=0, column=0, padx=5, pady=5)
entry_item = tk.Entry(frame2, width=30)
entry_item.grid(row=0, column=1, padx=5, pady=5)

label_inventory = tk.Label(frame2, text="Inventory:")
label_inventory.grid(row=1, column=0, padx=5, pady=5)
listbox_inventory = tk.Listbox(frame2, width=40)
listbox_inventory.grid(row=2, column=0, columnspan=3, padx=5, pady=5)


def add_item():
    """Adds the entered food item to the inventory list."""
    item = entry_item.get()
    if item:
        color = get_item_color(item)
        listbox_inventory.insert(tk.END, item)
        listbox_inventory.itemconfig(tk.END, fg=color)
        entry_item.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter a food item.")


def remove_item():
    """Removes the selected food item from the inventory list."""
    selected = listbox_inventory.curselection()
    if selected:
        listbox_inventory.delete(selected)
    else:
        messagebox.showerror("Error", "No item selected.")


def search_on_walmart():
    """Opens a new tab with the Walmart search results for the item."""
    item = entry_item.get()
    if item:
        search_query = urllib.parse.quote(item)
        url = f"https://www.walmart.ca/search?q={search_query}&c=10019"
        webbrowser.open(url)
    else:
        messagebox.showerror("Error", "Please enter a food item.")


btn_search_walmart = tk.Button(frame2, text="Search on Walmart",
                               command=search_on_walmart)
btn_search_walmart.grid(row=3, column=1, padx=5, pady=5)


def search_on_open_food_facts():
    """Opens a new tab with the Open Food Facts search results for the item."""
    item = entry_item.get()
    if item:
        search_query = urllib.parse.quote(item)
        url = ("https://world.openfoodfacts.org/cgi/search.pl?"
        + f"search_terms={search_query}&search_simple=1&action=process")
        webbrowser.open(url)
    else:
        messagebox.showerror("Error", "Please enter a food item.")


btn_search_open_food_facts = tk.Button(frame2, text="Search on Open Food Facts",
                                       command=search_on_open_food_facts)
btn_search_open_food_facts.grid(row=3, column=2)

btn_add = tk.Button(frame2, text="Add Item", command=add_item)
btn_add.grid(row=0, column=3)

btn_remove = tk.Button(frame2, text="Remove Item", command=remove_item)
btn_remove.grid(row=0, column=4)


def get_item_color(item):
    """Gets the color code (green or red) based on the item's expiration date.

    Args:
        item (str): The food item

    Returns:
        str: The color code for the item
    """
    response = requests.get(("https://world.openfoodfacts.org/cgi/search.pl?"
                             + f"search_terms={item}&search_simple=1&action="
                             + "process&json=1"))
    data = response.json()

    item_color = "black"

    if 'products' in data and len(data['products']) > 0:
        for product in data['products']:
            if 'nutriments' in product and 'nutrition-score-fr_100g' in product['nutriments']:
                nutriscore = int(product['nutriments']['nutrition-score-fr_100g'])
                if nutriscore <= 5:
                    item_color = "green"
                    break
                else:
                    item_color = "red"
                    break
            if 'nova_group' in product:
                nova_group = int(product['nova_group'])
                if nova_group <= 2:
                    item_color = "green"
                    break
                elif nova_group > 2:
                    item_color = "red"
                    break

    return item_color


def scan_barcode():
    """Scans a barcode using the camera and retrieves the name of the food item."""
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to access the camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray)

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            food_item = retrieve_food_item(barcode_data)
            if food_item:
                entry_item.delete(0, tk.END)
                entry_item.insert(tk.END, food_item)
                cap.release()
                cv2.destroyAllWindows()
                return
            else:
                print("Product not found")

        cv2.imshow("Barcode Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


btn_scan_barcode = tk.Button(frame2, text="Scan Barcode", command=scan_barcode)
btn_scan_barcode.grid(row=0, column=2)


def retrieve_food_item(barcode):
    """Retrieves the food item name from the Open Food Facts database using the barcode.

    Args:
        barcode (str): The barcode data.

    Returns:
        str: The name of the food item.
    """
    response = requests.get("https://world.openfoodfacts.org/api/v0/"
                            + f"product/{barcode}.json")
    data = response.json()
    if data['status'] == 1:
        return data['product']['product_name']
    return None


window.mainloop()
