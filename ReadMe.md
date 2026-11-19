# Inventory Management System API & CLI

A full-stack Python application built with Flask and a Command Line Interface (CLI) to manage an inventory database. It integrates with the Open Food Facts API to automatically fetch product details using a barcode.

## Features
- **Full CRUD Operations:** Create, Read, Update, and Delete inventory items via a RESTful Flask API.
- **External API Integration:** Fetches real-world product data (name, brand, ingredients) from the Open Food Facts API using a barcode.
- **In-Memory Database:** Uses a Python list (`mock_db`) to simulate persistent storage.
- **CLI Frontend:** A custom Python script (`cli.py`) that allows users to interact with the API directly from the terminal.

## Project Structure
- `app.py`: The Flask backend server containing all the RESTful routes.
- `cli.py`: The command-line interface that sends HTTP requests to the Flask app.
- `test_app.py` : The testing suite built with `pytest` to verify API endpoints.

## Installation & Setup
1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies
  ```bash
  pip install flask requests
  ```

## How to Run the Application
You must run the server and the CLI in two separate terminal windows.
**Terminal 1 (Starts the Server)**
```bash
python app.py
```
**Terminal 2 (Start the CLI)**
```bash
python cli.py
```
