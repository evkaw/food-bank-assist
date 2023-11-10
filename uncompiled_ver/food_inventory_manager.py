"""This file implements a GUI that allows the user to manage their food inventory.

It is able to create a list and based on the food item's nutritious and NOVA group
results, mark it green or red in font color (need or avoid for a food bank). It uses
the functionality of barcodes to scan an item and return a name to the search
field. Finally, it has quicklinks to the OpenFoodFacts & Walmart Grocery website for
accesibility.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from pyzbar.pyzbar import decode
import requests
import urllib.parse
import webbrowser

class FoodInventoryManagerGUI:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        label_item = tk.Label(self.parent, text="Food Item:")
        label_item.grid(row=0, column=0, padx=5, pady=5)
        entry_item = tk.Entry(self.parent, width=30)
        entry_item.grid(row=0, column=1, padx=5, pady=5)

        label_inventory = tk.Label(self.parent, text="Inventory:")
        label_inventory.grid(row=1, column=0, padx=5, pady=5)
        listbox_inventory = tk.Listbox(self.parent, width=40)
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


        btn_search_walmart = tk.Button(self.parent, text="Search on Walmart",
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


        btn_search_open_food_facts = tk.Button(self.parent, text="Search on Open Food Facts",
                                            command=search_on_open_food_facts)
        btn_search_open_food_facts.grid(row=3, column=2)

        btn_add = tk.Button(self.parent, text="Add Item", command=add_item)
        btn_add.grid(row=0, column=3)

        btn_remove = tk.Button(self.parent, text="Remove Item", command=remove_item)
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


        btn_scan_barcode = tk.Button(self.parent, text="Scan Barcode", command=scan_barcode)
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
