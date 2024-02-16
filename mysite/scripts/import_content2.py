import sqlite3
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def fetch_urls_to_scrape(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, url FROM news WHERE content = 'Error: ?' OR content = 'Error: ' OR TRIM(content) = '' OR content IS NULL OR content = ''")
    urls = cursor.fetchall()
    connection.close()
    return urls


def update_content_in_db(db_path, news_id, new_content):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("UPDATE news SET content = ? WHERE id = ?",
                   (new_content, news_id))
    connection.commit()
    connection.close()


def log_error_in_db(db_path, news_id, error_message):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("UPDATE news SET content = ? WHERE id = ?",
                   (f'Error: {error_message}', news_id))
    connection.commit()
    connection.close()


def scrape_page_content(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()

            # Добавляем куки
            context.add_cookies([
                {"name": "cookie_name1", "value": "cookie_value1", "url": url},
                {"name": "cookie_name2", "value": "cookie_value2", "url": url}
            ])

            page = context.new_page()

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "en-US,en;q=0.9"
            }

            page.evaluate(
                "(headers) => { Object.assign(document.documentElement.style, headers); }", headers)

            page.goto(url)

            page.wait_for_timeout(3000)

            page_content = page.content()

            browser.close()

        soup = BeautifulSoup(page_content, 'html.parser')
        paragraphs = soup.find_all('p')

        all_text = ' '.join(paragraph.get_text(strip=True)
                            for paragraph in paragraphs)

        return all_text
    except Exception as e:
        print(f"Error scraping page {url}: {e}")
        return None


def main():
    db_path = 'C:\\Users\\als19\\Desktop\\mysite\\db.sqlite3'
    urls_to_scrape = fetch_urls_to_scrape(db_path)
    for news_id, url in urls_to_scrape:
        new_content = scrape_page_content(url)
        if new_content is not None:
            update_content_in_db(db_path, news_id, new_content)
            print(f"News with ID {news_id} has been updated.")
        else:
            log_error_in_db(db_path, news_id,
                            f"Failed to scrape content from {url}.")
            print(f"Failed to update news with ID {news_id}. Logged error.")

    # Дополнительная проверка и заполнение 'Error: ??' для пустых новостей
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE news SET content = 'Error: ??' WHERE content IS NULL OR content = ''")
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
