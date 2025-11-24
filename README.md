# Medicine Price Tracker

## Project Overview

Access to affordable healthcare is often limited by the rising costs of essential medicines.
This project aims to scrape prices of essential medicines from multiple online pharmacies and provide a **dashboard** where people can **compare prices** and find the **most affordable sources**.

By making medicine price data transparent and easily accessible, we hope to empower individuals to make cost-effective healthcare decisions.

---

## Goals

* Scrape MRP, discount and final selling price for a user-entered medicine from major online pharmacies.
* Display the collected pricing data in a clear comparative table on a web dashboard.
* Allow users to download the comparison as a PDF for reference.

---

## Tech Stack

* **Backend / Scraping**: Python (Flask + Selenium)
* **Database**: SQLite
* **Frontend / Dashboard**: React.js + Typescript + Vite
* **API Calls**: REST API 
---

## Repository Structure (Final)

```
medicine_price_tracker/  # Root project directory
│
├── frontend and backend/   # Contains both backend server and frontend client
│   ├── backend/   # Python Flask backend for API and scraping
|   |   ├── apollo.py  # Scraper module for Apollo Pharmacy website
|   |   ├── app.py  # Main Flask application exposing REST API endpoints
|   |   ├── database.py  # Handles SQLite DB connection and queries
|   |   ├── medicines.db  # SQLite database storing medicine prices/data
|   |   ├── netmeds.py  # Scraper module for Netmeds website
|   |   ├── pharmeasy.py  # Scraper module for PharmEasy website
|   |   ├── requirements.txt  # Python dependencies to run backend
|   |   └── tata1mg_scrape.py  # Scraper module for Tata 1mg website
│   └── medicine_price_tracker_frontend/  # React frontend application
│       ├── src/  # Main source code
|       |   ├── assets/  # Images and static resources
|       |   |   ├──bg_image.png  # Background image used in UI
|       |   |   ├──logo.png  # App logo displayed in UI
|       |   |   └──react.svg  # React icon graphic
|       |   ├── components/  # UI components
|       |   |   ├──Body.tsx  # Main interface where search results appear
|       |   |   ├──Footer.tsx  # App footer layout component
|       |   |   ├──Header.tsx  # Navbar/header UI of the app
|       |   |   └──medicineResults.tsx  # Component to display scraped prices
|       |   ├── App.css  # Global styling for the React app
|       |   ├── App.tsx  # Root React component
|       |   ├── main.tsx  # Entry point that renders App into DOM
|       |   └── test.tsx  # Optional testing / demo component
|       ├── .gitignore  # Git ignored frontend files
|       ├── README.md  # Frontend-specific documentation
|       ├── eslint.config.js  # ESLint configuration for code quality
|       ├── index.html  # HTML root file Vite injects build output into
|       ├── package-lock.json  # NPM dependency lock file
|       ├── package.json  # Frontend dependencies and build scripts
|       ├── tsconfig.app.json  # TypeScript config for the app
|       ├── tsconfig.json  # Base TypeScript configuration
|       ├── tsconfig.node.json  # TS configuration for Node tooling
|       └── vite.config.ts  # Vite config for dev server & build
├── .gitignore  # Backend global ignore rules for Git
└── README.md  # Root/project-level documentation

```

---


## How to Run the Project

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/shuvranshu-halder/medicine_price_tracker.git
cd medicine_price_tracker
```

Go into the ```frontend and backend``` directory.


### 2️⃣ Backend Setup

```sh
cd backend
pip install -r requirements.txt
python app.py
```

Backend server will start successfully.



### 3️⃣ Frontend Setup

Open a **new terminal tab/window** and run:

```sh
cd medicine_price_tracker_frontend
npm install   # (Only required during first setup)
npm run dev
```

The frontend development server will start, and the terminal will show the exact URL. You can Ctrl+Click the link in the terminal to open it in your browser.



### Usage

* Enter any **medicine name** in the search box
* View price and availability results instantly
* Track **how many times** a medicine was searched
* Download results as **PDF**


---
