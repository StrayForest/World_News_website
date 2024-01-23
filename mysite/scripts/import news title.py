import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import logging
import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

locations = {
    "AR": "Argentina",
    "AU": "Australia",
    "AT": "Austria",
    "BE": "Belgium",
    "BR": "Brazil",
    "CA": "Canada",
    "CL": "Chile",
    "CO": "Colombia",
    "CZ": "Czechia",
    "DK": "Denmark",
    "EG": "Egypt",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GR": "Greece",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IN": "India",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IT": "Italy",
    "JP": "Japan",
    "KE": "Kenya",
    "MY": "Malaysia",
    "MX": "Mexico",
    "NL": "Netherlands",
    "NZ": "New Zealand",
    "NG": "Nigeria",
    "NO": "Norway",
    "PE": "Peru",
    "PH": "Philippines",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "RU": "Russia",
    "SA": "Saudi Arabia",
    "SG": "Singapore",
    "ZA": "South Africa",
    "KR": "South Korea",
    "ES": "Spain",
    "SE": "Sweden",
    "CH": "Switzerland",
    "TW": "Taiwan",
    "TH": "Thailand",
    "TR": "Türkiye",
    "UA": "Ukraine",
    "GB": "United Kingdom",
    "US": "United States",
    "VN": "Vietnam"
}

unique_articles = {}

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--ignore-certificate-errors')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def parse_search_count(search_count_str):
    # Удаление '+'
    search_count_str = search_count_str.replace('+', '')

    # Проверка и обработка для 'M' и 'K'
    if 'M' in search_count_str:
        return int(float(search_count_str.replace('M', '')) * 1000000)
    elif 'K' in search_count_str:
        return int(float(search_count_str.replace('K', '')) * 1000)
    else:
        return int(search_count_str)


def fetch_articles(loc, driver):
    articles = {}
    try:
        url = f"https://trends.google.com/trends/trendingsearches/daily?geo={loc}"
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "md-list.md-list-block"))
        )

        articles_elements = driver.find_elements(By.CSS_SELECTOR, "md-list.md-list-block")

        for article in articles_elements:
            title_parts = article.find_elements(By.CSS_SELECTOR, "div.details-wrapper div.details div.details-top div > span > a")
            summary_part = article.find_element(By.CSS_SELECTOR, "div.subtitles-text-wrapper.visible div.summary-text > a").text
            full_title = ' '.join([part.text for part in title_parts])
            search_count_element = article.find_element(By.CSS_SELECTOR, "div.search-count-title")
            search_count = parse_search_count(search_count_element.text)
            key = (full_title, summary_part)
            if key not in articles or articles[key]["search_count"] < search_count:
                articles[key] = {
                    "title": full_title,
                    "description": summary_part,
                    "country_code": loc,
                    "search_count": search_count
                }
    except TimeoutException:
        logger.info(f"Тайм-аут при ожидании загрузки статей для {loc}")
    except Exception as e:
        logger.error(f"Ошибка при извлечении статей для {loc}: {e}")
    finally:
        driver.quit()
    return articles

def insert_into_db(article_title, article_description, country_name, search_count):
    try:
        if country_name == "United States":
            country_name = "USA"

        with sqlite3.connect(r'C:\Users\als19\Desktop\mysite\db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM news WHERE title = ? AND description = ?", (article_title, article_description))
            exists = cursor.fetchone()[0] > 0
            if not exists:
                current_datetime = datetime.datetime.now()
                formatted_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S') # Преобразование datetime в строку
                cursor.execute("INSERT INTO news (title, description, country_name, searches, date) VALUES (?, ?, ?, ?, ?)",
                               (article_title, article_description, country_name, search_count, formatted_date))
    except sqlite3.Error as e:
        logger.error(f"Ошибка SQLite: {e}")

async def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        for loc in locations.keys():
            driver = create_driver()
            task = loop.run_in_executor(executor, fetch_articles, loc, driver)
            tasks.append(task)
        results = await asyncio.gather(*tasks)

        for articles in results:
            for key, article_info in articles.items():
                if key not in unique_articles or unique_articles[key]["search_count"] < article_info["search_count"]:
                    unique_articles[key] = article_info

        for article_info in unique_articles.values():
            title = article_info['title']
            description = article_info['description']
            country_code = article_info['country_code']
            country_name = locations[country_code]
            search_count = article_info['search_count']
            insert_into_db(title, description, country_name, search_count)

if __name__ == "__main__":
    asyncio.run(main())