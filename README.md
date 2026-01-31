# 🏭 MartScout AI: Indiamart B2B Scraper

A clean, modular web scraper for Indiamart B2B product listings, built with Python and structured using a clean architecture approach.

This scraper allows you to extract key product data (like titles, prices, ratings, and company names) and explore it via a user-friendly Streamlit interface. It also includes an AI-powered recommendation agent using Gemini.

---

## 🚀 Features

- 🔍 Search for any product on Indiamart by keyword
- 🧠 Clean and maintainable architecture (controllers, models, enums, helpers)
- 🖥️ Streamlit UI for interactive use
- 🤖 AI-powered "Best Deal" recommendation using Google Gemini

---

## 📁 Project Structure

Scraper/

├── Agents/
│   └── Agent_feedback.py     # AI Agent logic for recommendations
├── Controllers/
│   └── scraper_controller.py # Handles Indiamart scraping logic
├── Helpers/
│   └── config.py             # Configuration (API Keys etc)
│   └── scraper_utils.py      # Utility functions
├── LLM/
│   └── gemini_client.py      # Google Gemini wrapper
├── Products/
│   └── product.py            # Dataclasses for structured product data
├── Styles/                   # CSS for Streamlit
├── app.py                    # Streamlit interface
├── main.py                   # Entrypoint for CLI use (optional)
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview

---

## 🧪 Quickstart

### 1. Create virtual environment

```bash
conda create --name Scraper
conda activate Scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 🧰 Tech Stack

- **Python**
- **BeautifulSoup4** – HTML parsing
- **Requests** – HTTP client
- **Streamlit** – UI
- **Google Gemini** – LLM Integration
- **Pandas** – Data manipulation

---

## 🎯 Objective

The primary objective of this project is to automate the retrieval and analysis of B2B product data from **Indiamart**, India's largest B2B marketplace. The tool streamlines the process of finding suppliers, comparing prices, and identifying the best value deals using Artificial Intelligence.

## 💼 Business Problem Solved

1.  **Inefficient Market Research**: Manual searching on Indiamart is time-consuming and difficult to organize. This tool aggregates data instantly.
2.  **Price Transparency**: By extracting prices across multiple listings, businesses can easily benchmark market rates.
3.  **Supplier Vetting**: The tool captures company names and ratings, aiding in the preliminary vetting of suppliers.
4.  **Decision Paralysis**: With hundreds of options, choosing the "best" one is hard. The integrated **AI Agent** provides an unbiased, data-driven recommendation to speed up procurement decisions.

## 🛠️ Technology Stack Breakdown

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.x | Core logic and scripting |
| **Web Scraping** | BeautifulSoup4, Requests | Parsing HTML and handling HTTP requests |
| **Frontend** | Streamlit | Interactive user interface for searching and viewing data |
| **Data Handling** | Pandas | structured data manipulation and CSV export |
| **AI/LLM** | Google Gemini (via `google-generativeai`) | Analyzes product data to recommend the best deal |
| **Architecture** | MVC (Model-View-Controller) | Modular code structure for maintainability |

## 🔮 Future Enhancements

-   **Multi-page Scraping**: Extend capability to scrape multiple pages of results.
-   **Proxy Rotation**: Implement ScrapeOps or similar services to avoid IP bans at scale.
-   **Authentication**: Add user login to save search history.





