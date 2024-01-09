# Food Bank Assist (Food Bank Locator & Food Inventory Generator)

## Install from [releases](https://github.com/evkaw/food-bank-assist/releases/tag/release) for newest application. (no API key required!)

### Android:

<img src="https://github.com/evkaw/food-bank-assist/blob/main/image4.png" width=20% height=20%> <img src="https://github.com/evkaw/food-bank-assist/blob/main/image1.png" width=20% height=20%> <img src="https://github.com/evkaw/food-bank-assist/blob/main/image3.png" width=20% height=20%> <img src="https://github.com/evkaw/food-bank-assist/blob/main/image5.png" width=20% height=20%>

https://github.com/evkaw/food-bank-assist/assets/82726788/000295ae-17f0-4636-9f9e-91f69440576f

### MacOS, Linux, Windows (Windows will look similar)
<img src="https://github.com/evkaw/food-bank-assist/assets/82726788/ad2239b2-e7e0-48a7-878c-244486c4f3bb" width=33% height=33%><img src="https://github.com/evkaw/food-bank-assist/assets/82726788/ac161f30-5ea0-4069-a22f-740552dc2c05" width=33% height=33%><img src="https://github.com/evkaw/food-bank-assist/assets/82726788/70316412-8d7b-41e3-8723-748e4861e7fd" width=33% height=33%>

## Usage

### Food Bank Locator:

- Enter your location manually or click the "Autogenerate Location" button to generate your location automatically.
- Choose a search radius or select a preselected radius option.
- Click the "Search Food Banks" button to retrieve nearby food banks.
- The food banks will be displayed in the listbox. Double-click on a food bank to open its location on Google Maps.

### Food Inventory Generator:

- Enter a food item in the "Food Item" field and click the "Add Item" button to add it to the inventory.
- Select an item from the inventory list and click the "Remove Item" button to remove it from the inventory.
- Click the "Search on Walmart" button to search for the entered food item on Walmart's online grocery section.
- Click the "Search on Open Food Facts" button to search for the entered food item on Open Food Facts's online database.
- Click the "Scan Barcode" button to scan a barcode using your computer's camera and retrieve the food item information.

- The entered-in/scanned food item will be marked green or red in font color based on its nutritious values & it's grade on the NOVA scale, which ranks foods for their processed levels.

## Styling

[PEP8](https://peps.python.org/pep-0008/) standard has been used for this version of the program.

### Warning

Trying to compile the program yourself instead of using [`food_bank_assist.py`](https://github.com/evkaw/food-bank-assist/blob/main/food_bank_assist.py) might result in unexpected errors/complications; so please use this file for execution.

## Manual Build Instructions
1. Install the required libraries using `pip install -r requirements.txt`
2. Obtain a [Google Maps API key](https://developers.google.com/maps/documentation/embed/get-api-key) & enter it for the `API_KEY` constant in the [`food_bank_assist.py`](https://github.com/evkaw/food-bank-assist/blob/main/food_bank_assist.py) file.
