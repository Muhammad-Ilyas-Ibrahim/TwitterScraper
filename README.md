
# 🐦 TwitterScraper

TwitterScraper is a Python script that lets you scrape data from Twitter with ease. Whether you're looking to analyze tweet content, monitor engagement, or gather insights, this tool simplifies the process. It automates the login process and retrieves tweet details such as text, date, time, views, likes, reposts, quotes, and replies.

![TwitterScraper in Action](twitter_scraper.gif)

## 🚀 Features

- **Automated Login:** TwitterScraper streamlines the login process, allowing you to access data from your Twitter account conveniently.

- **Data Scraping:** Gather information from tweets on your chosen Twitter account, including the text, date, time, views, likes, reposts, quotes, and replies.

- **Customizable:** Modify parameters such as the Twitter account URL and the number of scrolls to collect the desired amount of data.

- **Export to Excel:** Save the collected data in an Excel file for further analysis.

## 📋 Prerequisites

Before you get started, make sure you have the following prerequisites:

- [Python](https://www.python.org/) (version 3.6 or higher)
- [Playwright](https://playwright.dev/python/) (installed using `pip`)
- [Beautiful Soup 4 (bs4)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (installed using `pip`)
- [Pandas](https://pandas.pydata.org/) (installed using `pip`)

You can install these dependencies with the following commands:

```bash
pip install playwright
pip install bs4 pandas
```

## 📦 Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Muhammad-Ilyas-Ibrahim/TwitterScraper.git
```

2. Navigate to the project directory:

```bash
cd TwitterScraper
```

3. Run the script and follow the on-screen prompts:

```bash
python main.py
```

## 💡 Usage

1. **Login:** Select option 1 to log in to your Twitter account. This step is necessary to access Twitter data.

2. **Scrape Data:** Select option 2 to scrape data from a Twitter account. Provide the URL of the Twitter account you want to scrape, specify the number of scrolls to collect tweets, and more.

3. **Scrape Unloaded URLs:** Select option 3 to scrape URLs that were not loaded in a previous run.

4. **Export Data:** The scraped data is automatically exported to an Excel file for further analysis.

## 🤝 Contributing

If you'd like to contribute to this project, have suggestions, or encounter issues, please feel free to open an [issue](https://github.com/Muhammad-Ilyas-Ibrahim/TwitterScraper/issues) or submit a [pull request](https://github.com/Muhammad-Ilyas-Ibrahim/TwitterScraper/pulls).
