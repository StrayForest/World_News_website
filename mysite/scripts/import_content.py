import subprocess
import aiohttp
import asyncio
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from aiohttp import TCPConnector
from bs4 import BeautifulSoup
import time

# Объявление глобальной переменной
time_sleep = 0

def connect_to_database():
    return sqlite3.connect(r'C:\Users\als19\Desktop\mysite\db.sqlite3')


def initialize_webdriver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    return webdriver.Chrome(options=chrome_options)


async def scrape_news_content(news_id, news_url, time_sleep):
    max_attempts = 2  # Максимальное количество попыток сбора информации
    attempts = 0

    while attempts < max_attempts:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }

            connector = TCPConnector(ssl=False)  # Отключаем проверку SSL
            async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
                async with session.get(news_url, timeout=30) as response:
                    page_content = await response.text()

            time.sleep(time_sleep)

            soup = BeautifulSoup(page_content, 'html.parser')

            # Найти все теги "p"
            all_paragraphs = soup.find_all('p')

            # Найти текст только из тегов "p", находящихся до тега "footer"
            content = ''
            for paragraph in all_paragraphs:
                if paragraph.find_parent('footer'):
                    break  # Прерываем, если достигли тега "footer"
                content += paragraph.get_text(strip=True) + ' '

            # Обновление записи в базе данных с собранным содержимым
            c.execute("UPDATE news SET content = ? WHERE id = ?",
                      (content, news_id))
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
            c.execute("UPDATE news SET content = ? WHERE id = ?",
                      (f"Error: {str(e)}", news_id))
            conn.commit()
            print(f"Достигнуто максимальное количество попыток для новости с ID {news_id}.")


async def main():
    global time_sleep  # Объявление, что используется глобальная переменная
    # Получение списка уникальных URL с пустым контентом
    c.execute("SELECT id, url FROM news WHERE content IS NULL OR content = ''")
    unique_news = c.fetchall()

    # Запуск задач для новостей с пустым контентом сразу
    tasks = [scrape_news_content(news_id, news_url, time_sleep) for news_id, news_url in unique_news]
    await asyncio.gather(*tasks)

    # После первой попытки
    # Добавление задержки в 3 секунды
    await asyncio.sleep(3)

    time_sleep = 3  # Обновление переменной

    # Повторное получение списка уникальных URL с пустым контентом
    c.execute("SELECT id, url FROM news WHERE content IS NULL OR content = ''")
    unique_news = c.fetchall()

    # Запуск задач для новостей с пустым контентом с задержкой
    tasks = [scrape_news_content(news_id, news_url, time_sleep) for news_id, news_url in unique_news]
    await asyncio.gather(*tasks)

    # После второй попытки
    # Заполнение пустых записей в базе данных
    c.execute(
        "UPDATE news SET content = ? WHERE content IS NULL OR content = ''", ('Error: ?',))
    conn.commit()

    print("Запуск скрипта...")
    subprocess.run(["python", "C:\\Users\\als19\\Desktop\\mysite\\scripts\\# test.py"])
    print("Скрипт успешно выполнен.")

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
