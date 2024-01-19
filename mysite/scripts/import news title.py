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


def fetch_articles(loc, driver, articles):
    try:
        url = f"https://trends.google.com/trends/trendingsearches/daily?geo={loc}"
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "md-list.md-list-block"))
            )
        except TimeoutException:
            print(f"Тайм-аут при ожидании загрузки статей для {loc}")
            return

        articles_elements = driver.find_elements(
            By.CSS_SELECTOR, "md-list.md-list-block")
        
        for article in articles_elements:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "div.details-wrapper div.details div.details-top div > span > a"))
                )
                title_parts = article.find_elements(
                    By.CSS_SELECTOR, "div.details-wrapper div.details div.details-top div > span > a")
                summary_part = article.find_element(
                    By.CSS_SELECTOR, "div.subtitles-text-wrapper.visible div.summary-text > a").text

                full_title = ' '.join([part.text for part in title_parts])

                search_count_element = article.find_element(
                By.CSS_SELECTOR, "div.search-count-title")
                search_count = parse_search_count(search_count_element.text)

                key = (full_title, summary_part)

                # Создаем словарь для хранения названия статьи, описания и кода страны
                if key not in unique_articles or unique_articles[key]["search_count"] < search_count:
                    article_info = {
                        "title": full_title,
                        "description": summary_part,
                        "country_code": loc,
                        "search_count": search_count
                    }
                    unique_articles[key] = article_info

            except Exception as e:
                print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

def insert_into_db(article_title, article_description, location, search_count):
    conn = None
    try:
        conn = sqlite3.connect(r'C:\Users\als19\Desktop\mysite\db.sqlite3')
        cursor = conn.cursor()

        # Проверяем, существует ли уже такая новость в базе данных
        query_check = """SELECT COUNT(*) FROM news WHERE title = ? AND description = ?"""
        cursor.execute(query_check, (article_title, article_description))
        exists = cursor.fetchone()[0] > 0

        # Если новость не существует, добавляем ее в базу данных
        if not exists:
            query_insert = """INSERT INTO news (title, description, country_article, searches) VALUES (?, ?, ?, ?)"""
            cursor.execute(query_insert, (article_title, article_description, location, search_count))
            conn.commit()

    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")
    finally:
        if conn:
            conn.close()

async def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        for loc in locations.keys():  # Используем только ключи из словаря locations
            driver = create_driver()
            task = loop.run_in_executor(
                executor, fetch_articles, loc, driver, unique_articles)
            tasks.append(task)
        await asyncio.gather(*tasks)

    for key, article in unique_articles.items():
        title = article['title']
        description = article['description']
        country_code = article['country_code']
        search_count = article['search_count']
        insert_into_db(title, description, country_code, search_count)

if __name__ == "__main__":
    asyncio.run(main())
