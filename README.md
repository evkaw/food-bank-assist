# Charity Finder (Food Bank Locator & Food List Generator)

## Install from [releases](https://github.com/evkaw/charity-finder/releases/tag/release) for Android. (no API key required!)

<img src="https://github.com/evkaw/charity-finder/blob/main/image4.png" width=20% height=20%> <img src="https://github.com/evkaw/charity-finder/blob/main/image1.png" width=20% height=20%> <img src="https://github.com/evkaw/charity-finder/blob/main/image3.png" width=20% height=20%> <img src="https://github.com/evkaw/charity-finder/blob/main/image5.png" width=20% height=20%>

Uploading android_sample.mp4…

## Instructions (for MacOS, Windows & Linux)
1. Install the required libraries using `pip install -r requirements.txt`
2. Obtain a [Google Maps API key](https://developers.google.com/maps/documentation/embed/get-api-key) & enter it for the `API_KEY` constant in the [`food_bank_locator.py`](https://github.com/evkaw/food-bank-locator/blob/main/food_bank_locator.py) file.

## Usage

### Food Bank Locator:

- Enter your location manually or click the "Autogenerate Location" button to generate your location automatically.
- Choose a search radius or select a preselected radius option.
- Click the "Search Food Banks" button to retrieve nearby food banks.
- The food banks will be displayed in the listbox. Double-click on a food bank to open its location on Google Maps.

### Food Inventory:

- Enter a food item in the "Food Item" field and click the "Add Item" button to add it to the inventory.
- Select an item from the inventory list and click the "Remove Item" button to remove it from the inventory.
- Click the "Search on Walmart" button to search for the entered food item on Walmart's online grocery section.
- Click the "Search on Open Food Facts" button to search for the entered food item on Open Food Facts's online database.
- Click the "Scan Barcode" button to scan a barcode using your computer's camera and retrieve the food item information.

- The entered-in/scanned food item will be marked green or red in font color based on its nutritious values & it's grade on the NOVA scale, which ranks foods for their processed levels.

## Styling

[PEP8](https://peps.python.org/pep-0008/) standard has been used for this version of the program.

### Warning

Trying to compile the program yourself instead of using [`food_bank_locator.py`](https://github.com/evkaw/food-bank-locator/blob/main/food_bank_locator.py) might result in unexpected errors/complications; so please use this file for execution.
