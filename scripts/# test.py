from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def scrape_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        # Открываем новую страницу с контекстом
        page = context.new_page()

        # Задаем заголовки, включая user agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Имитируем заголовки, включая user agent
        page.evaluate(
            "(headers) => { Object.assign(document.documentElement.style, headers); }", headers)

        # Открываем страницу
        page.goto(url)

        # Даем странице время на загрузку
        # Подождем 5 секунд (вы можете изменить это значение)
        page.wait_for_timeout(3000)

        # Получаем содержимое страницы
        page_content = page.content()

        # Закрываем браузер
        browser.close()

    # Теперь вы можете использовать BeautifulSoup или другие инструменты для обработки содержимого
    soup = BeautifulSoup(page_content, 'html.parser')
    paragraphs = soup.find_all('p')

    # Извлекаем текст из каждого параграфа и объединяем весь текст
    all_text = ' '.join(paragraph.get_text(strip=True)
                        for paragraph in paragraphs)

    return all_text

# Пример использования функции


print(scrape_page_content(
    'https://www.svenskafans.com/europa/ajax/ajax-1-1-psv-oavgjort-i-hendersons-debut-666360'))
