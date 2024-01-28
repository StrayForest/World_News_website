import aiohttp
import asyncio
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def connect_to_database():
    return sqlite3.connect(r'C:\Users\als19\Desktop\mysite\db.sqlite3')

def initialize_webdriver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    return webdriver.Chrome(options=chrome_options)

async def scrape_news_content(news_id, news_url, session):
    max_attempts = 2  # Максимальное количество попыток сбора информации
    attempts = 0

    while attempts < max_attempts:
        try:
            async with session.get(news_url) as response:
                page_content = await response.text()

            soup = BeautifulSoup(page_content, 'html.parser')
            text_blocks = soup.find_all(['p'])
            content = ' '.join(block.get_text(strip=True) for block in text_blocks if block.get_text(strip=True))

            # Обновление записи в базе данных с собранным содержимым
            c.execute("UPDATE news SET content = ? WHERE id = ?", (content, news_id))
            conn.commit()

            print(f"Новость с ID {news_id} обновлена успешно.")
            break  # Выход из цикла после успешного сбора информации

        except Exception as e:
            attempts += 1
            print(f"Попытка {attempts}: Ошибка при обработке новости с ID {news_id}: {e}")

            if attempts < max_attempts:
                # Если есть еще попытки, обновляем страницу и продолжаем
                print("Обновление страницы...")
                continue

            # Если все попытки использованы, записываем ошибку в content
            c.execute("UPDATE news SET content = ? WHERE id = ?", (f"Error: {str(e)}", news_id))
            conn.commit()
            print(f"Достигнуто максимальное количество попыток для новости с ID {news_id}.")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_news_content(news_id, news_url, session) for news_id, news_url in unique_news]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    conn = connect_to_database()
    c = conn.cursor()

    # Получение списка уникальных URL с пустым контентом
    c.execute("SELECT id, url FROM news WHERE content IS NULL OR content = ''")
    unique_news = c.fetchall()

    # Инициализация WebDriver
    driver = initialize_webdriver()

    try:
        asyncio.run(main())
    finally:
        # Закрытие WebDriver и соединения с базой данных
        driver.quit()
        conn.close()
