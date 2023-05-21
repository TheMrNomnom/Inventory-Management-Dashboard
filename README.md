# Inventory Management System

This is a multi-file Python program that implements an Inventory Management System using the Flask web framework. The system allows users to manage inventory items, track their quantities, and associate them with specific locations. It also provides endpoints for retrieving item and location information through API calls. This web application allows users to manage inventory items and locations. It provides features for adding, editing, and deleting items and locations, as well as a price variance calculator. The application is built using HTML, CSS, and JavaScript, with the Flask framework handling the server-side logic.

## Prerequisites

- Python 3.x
- Flask
- Flask SQLAlchemy
- Flask Session
- Flask Login

## Getting Started

To run the program, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <repository-folder>`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Set up the database: `python -m website`
5. Start the Flask development server: `python main.py`
6. Open your web browser and go to `http://localhost:5000`

## Program Structure

The program consists of several Python files organized into a package named `website`. Here is an overview of the file structure:

- `main.py`: The main entry point of the application. It creates and runs the Flask app.
- `website/__init__.py`: Initializes the Flask app and sets up the database connection, session, and routing.
- `website/auth.py`: Contains routes and functions for user authentication (login, logout, registration).
- `website/endpoints.py`: Provides API endpoints for retrieving item and location information.
- `website/helpers.py`: Contains helper functions used throughout the application.
- `website/models.py`: Defines the database models for User, Item, and Location using SQLAlchemy.
- `website/views.py`: Defines the routes and functions for rendering HTML templates and managing inventory.

## Features

The Inventory Management System provides the following features:

- User authentication: Users can register, log in, and log out.
- Homepage: Displays all items in the inventory, their quantities, and associated locations.
- Add inventory or locations: Allows users to add new items or locations to the database.
- Edit inventory entries: Users can update the quantity and location of existing items.
- Delete inventory: Allows users to remove items from the inventory, optionally reassigning them to a different location.
- Variance calculator: Provides a page for calculating the variance of item quantities.

## API Endpoints

The program offers the following API endpoints:

- `/item_info`: Returns information about a specific item based on the item ID.
- `/location_info`: Returns the location of an item based on the item ID.

To access these endpoints, you need to be logged in.

## HTML Templates

### layout.html

This template defines the overall structure and layout of the web pages. It includes a navigation bar, a header for displaying flash messages, and a main content section where other templates can be extended.

### add.html

The add.html template extends the layout.html template and provides a form for adding new items and locations. It includes input fields for item name, quantity, and location selection.

### delete.html

The delete.html template extends the layout.html template and provides options for deleting items and locations. It includes dropdown menus for selecting items and locations to be deleted.

### edit.html

The edit.html template extends the layout.html template and allows users to edit item details, such as quantity and location. It includes dropdown menus for selecting the item to be edited and the new location.

### index.html

The index.html template extends the layout.html template and displays a table of inventory items. It shows the item name, quantity, and location.

### login.html

The login.html template extends the layout.html template and provides a form for user login. It includes input fields for username and password.

### register.html

The register.html template extends the layout.html template and provides a form for user registration. It includes input fields for username, password, and password confirmation.

### variance_calculator.html

The variance_calculator.html template extends the layout.html template and provides a form for calculating price variance. It includes dropdown menus for selecting the item, input fields for desired quantity and standard cost per unit, and displays the current quantity and price variance per unit.
