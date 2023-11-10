"""This module implements a graphical user interface that allows users 
to find nearby food banks and manage their food inventory."""

import tkinter as tk
from tkinter import ttk
from food_bank_locator import FoodBankLocatorGUI
from food_inventory_manager import FoodInventoryManagerGUI

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

FoodBankLocatorGUI(frame1)
FoodInventoryManagerGUI(frame2)

window.mainloop()
