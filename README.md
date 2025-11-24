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
medicine_price_tracker/
│
├── frontend and backend/         
│   ├── backend/
|   |   ├── apollo.py
|   |   ├── app.py
|   |   ├── database.py
|   |   ├── medicines.db
|   |   ├── netmeds.py
|   |   ├── pharmeasy.py
|   |   ├── requirements.txt
|   |   └── tata1mg_scrape.py 
│   └── medicine_price_tracker_frontend/           
│       ├── src/
|       |   ├── assets/
|       |   |   ├──bg_image.png
|       |   |   ├──logo.png
|       |   |   └──react.svg
|       |   ├── components/
|       |   |   ├──Body.tsx
|       |   |   ├──Footer.tsx
|       |   |   ├──Header.tsx
|       |   |   └──medicineResults.tsx
|       |   ├── App.css
|       |   ├── App.tsx
|       |   ├── main.tsx
|       |   └── test.tsx
|       ├── .gitignore
|       ├── README.md
|       ├── eslint.config.js
|       ├── index.html
|       ├── package-lock.json
|       ├── package.json
|       ├── tsconfig.app.json
|       ├── tsconfig.json
|       ├── tsconfig.node.json
|       └── vite.config.ts
├── .gitignore
└── README.md
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
