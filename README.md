# 💊 Medicine Price Tracker

## 📌 Project Overview

Access to affordable healthcare is often limited by the rising costs of essential medicines.\  
This project aims to scrape prices of essential medicines from multiple online pharmacies and provide a **dashboard** where people can **compare prices** and find the **most affordable sources**.  

By making medicine price data transparent and easily accessible, we hope to empower individuals to make cost-effective healthcare decisions.

---

## 🎯 Goals

- Scrape medicine prices from multiple online pharmacy websites based on user input.
- Store and maintain updated price data.
- Build a web-based dashboard for comparing prices.
- Provide search and filtering options for essential medicines.
- Ensure scalability and accuracy of the data pipeline.

---

## 🛠️ Tech Stack (Planned)

- **Backend / Scraping**: Python (Flask + BeautifulSoup)  
- **Database**: SQLite (initial), upgradeable to PostgreSQL/MongoDB  
- **Frontend / Dashboard**: React.js with Axios for API calls
- **Deployment**: Vercel (Not finalised yet)

---

## 📂 Repository Structure (Planned)

```
medicine_price_tracker/
│
├── backend/                 # Flask API and database management
│   ├── app.py               # Flask app and API routes
│   └── database/            # DB creation and management
│       └── create_database.ipynb
│
├── frontend/                # React frontend application
│   ├── package.json
│   ├── src/
│   │   ├── components/      # React components
│   │   └── App.js
│   └── public/
│
├── data/                    # Scraped and processed datasets
│   ├── raw/                 # Raw HTML/JSON from scrapers
│   └── medicines.db         # SQLite database for Flask API
│
├── docs/                    # Documentation and reports
│
├── src/                     # Jupyter notebooks for scraping and testing
│   ├── scraper.ipynb        # Combined scrapers for user input medicines
│   └── tests/               # Unit & integration tests
│       ├── test_scraper.ipynb
│       ├── test_database.ipynb
│       └── test_api_routes.ipynb
│
├── requirements.txt         # Python dependencies
└── README.md                # Project overview
```

---

## 📜 License

This project will be open-sourced under the **MIT License**.

---

## 📎 Links

🔗 GitHub Repository: [Medicine Price Tracker](https://github.com/shuvranshu-halder/medicine_price_tracker)

---
