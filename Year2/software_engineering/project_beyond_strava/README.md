# Group_01_Mecchia_Nicolet
## 🚀 Project Overview

Welcome to our client-server application designed to empower advanced analysis of personal fitness data from Strava! This project blends a Flask web service, MongoDB Atlas backend, and a Python client library for seamless data retrieval and processing.

---

## 🛠️ How It Works

### Step 1: Populate the Database  
Our journey begins with running `populate_db.py`. This script seeds our MongoDB Atlas database with Strava fitness data — the foundation for all future analysis.

### Step 2: The Web Service  
The `web_service` package is the heart of our backend:

- Manages **two main collections**:  
  - `athlete` — stores athlete profiles  
  - `activities` — stores activity records linked to athletes via `athlete_id` foreign key  
- Implements RESTful API routes supporting **GET, POST, PUT, DELETE** operations on both collections  
- Returns all data in clean JSON format for easy consumption

### Step 3: The Client Library  
`client_lib` is our Python client package that:

- Makes HTTP requests to the Flask web service  
- Transforms JSON responses into Python dictionaries and objects  
- Provides reusable functions to retrieve and process athlete and activity data  

### Step 4: Utility Scripts & Demo  
- Utility scripts (`utils_*.py`) contain helper functions to analyze and manipulate the data  
- `demo.py` offers an interactive CLI menu for managing athletes, activities, and performing advanced analyses — giving you a hands-on experience  

---

## 🎯 Features at a Glance

- **Database setup** via `populate_db.py`  
- **Fully functional Flask REST API** supporting CRUD operations on athletes and activities  
- **Client library** wrapping API calls with data parsing utilities  
- **Command-line interface** to interact with your data seamlessly  
- Modular structure allowing easy maintenance and expansion  

---

## ⚙️ Installation & Usage

1. **Populate the database:**  
   ```bash
   python scripts/populate_db.py
   ```

2. **Start the Flask server in the first terminal:**
    ```bash
   python run.py
   ```

3. **Run the demo CLI in a second terminal:**
    ```bash
   python demo.py
   ```
   

## 📋 Requirements
    - Python 3.10
    - Flask
    - pymongo
    - mongoengine
    - python-dotenv
    - requests
    - matplotlib