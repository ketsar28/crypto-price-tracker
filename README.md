# Crypto Price Tracker - A Streamlit Web Application

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_HUGGINGFACE_SPACE_URL)
[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](YOUR_HUGGINGFACE_SPACE_URL)

A real-time cryptocurrency price tracking dashboard built with Streamlit. This application scrapes data for the top 100 cryptocurrencies from CoinMarketCap and presents it in a clean, interactive, and visually appealing user interface.


![App Screenshot](https://github.com/user-attachments/assets/21ade05d-00cd-4b18-b901-67c6f5b9fbc3)

---

# 📋 Features

-   **Real-Time Data**: Fetches the latest price data for the top 100 cryptocurrencies.
-   **Multi-Currency Support**: View prices in various fiat and crypto currencies (USD, IDR, BTC, ETH).
-   **Interactive Dashboard**: Filter by specific cryptocurrencies, select the number of top coins to display, and sort data based on performance.
-   **At-a-Glance Metrics**: Key performance indicators (KPIs) for top selected coins are displayed prominently using metrics cards.
-   **Rich Data Visualization**:
    -   A styled and formatted data table with conditional coloring for price changes and a color gradient for market capitalization.
    -   An interactive bar chart to visualize percentage price changes over different timeframes (1h, 24h, 7d).
    -   A pie chart showing the market cap distribution of the selected cryptocurrencies.
-   **Data Export**: Download the filtered data as a CSV file for offline analysis.
-   **Responsive Design**: A clean, tabbed interface that works well on different screen sizes.

---

# 🛠️ Tech Stack

-   **Framework**: Streamlit
-   **Data Manipulation**: Pandas
-   **Web Scraping**: Requests, BeautifulSoup4
-   **Data Visualization**: Plotly Express
-   **Deployment**: Hugging Face Spaces

---

# 🚀 Getting Started

##  Prerequisites

-   Python 3.8+
-   An IDE or code editor (e.g., VS Code, Spyder)
-   Git

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ketsar28/crypto-price-tracker.git
    cd crypto-price-tracker
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    The application should now be running in your local browser!

---


## 2. Ensure Your File Structure is Correct

Your project directory should contain at least these files:

```
├── 📄 app.py              # Your main application script
├── 📄 requirements.txt    # The list of dependencies
├── 🖼️ logo.jpg            # The logo image file
```
