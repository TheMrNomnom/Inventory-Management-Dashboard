# Inventory Management Dashboard

This is a Python Flask web application that serves as an inventory management system. It allows users to add, edit, and delete items and locations in the inventory. The application provides a user authentication system for secure access to the inventory management functionality.

## Getting Started

To run this application, follow the steps below:

1. Clone the repository: `git clone https://github.com/TheMrNomnom/Inventory-Management-Dashboard.git`
2. Change to the project directory: `cd inventory-management-dashboard`

### Prerequisites

Make sure you have the following software installed:

- Python 3
- pip (Python package installer)

### Installation

1. Create a virtual environment (optional but recommended): `python3 -m venv venv`
2. Activate the virtual environment (optional): 
   - For macOS/Linux: `source venv/bin/activate`
   - For Windows: `venv\Scripts\activate.bat`
3. Install the required dependencies: `pip install -r requirements.txt`

### Usage

Run the Flask development server:

```bash
python main.py
```

The application will be accessible at [http://localhost:5000](http://localhost:5000).

## Functionality

The application provides the following functionality:

- User authentication: Users can register, log in, and log out.
- View inventory: Users can view all items in the inventory, their quantity, and their location.
- Add item/location: Users can add new items or locations to the inventory.
- Edit item/location: Users can edit existing items or locations in the inventory.
- Delete item/location: Users can delete items or locations from the inventory.

## Project Structure

The project is structured as follows:

- `main.py`: The main entry point of the application. It creates and runs the Flask app.
- `website/`:
  - `__init__.py`: Initializes the Flask app and sets up the database and session configurations.
  - `views.py`: Defines the routes and views for the web pages.
  - `auth.py`: Handles user authentication-related routes.
  - `endpoints.py`: Provides endpoints for retrieving item and location information.
  - `models.py`: Defines the database models using SQLAlchemy.
  - `helpers.py`: Contains helper functions used in the views and models.
- `templates/`: Contains HTML templates used to render the web pages.
- `static/`: Contains static files such as CSS stylesheets and JavaScript files.

## Dependencies

The project has the following dependencies:

- Flask: A micro web framework for Python.
- Flask SQLAlchemy: Provides SQLAlchemy integration for Flask.
- Flask Session: Adds support for server-side sessions in Flask.
- Flask Login: Handles user authentication and session management.

These dependencies are specified in the `requirements.txt` file.

## HTML and CSS Files

### website/add.html

This file contains the HTML and CSS code for adding items and locations.

### website/delete.html

This file contains the HTML and CSS code for deleting items and locations.

### website/edit.html

This file contains the HTML and CSS code for editing items and locations.

### website/index.html

This file contains the HTML and CSS code for the home page, which displays the inventory items.

### website/layout.html

This file contains the HTML and CSS code for the layout template used throughout the web application.

### website/login.html

This file contains the HTML and CSS code for the login page.

### website/register.html

This file contains the HTML and CSS code for the registration page.

### website/variance_calculator.html

This file contains the HTML and CSS code for the variance calculator page.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
