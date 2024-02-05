import re
import sqlite3
import g4f
import time

g4f.debug.logging = True
g4f.debug.version_check = False

# Создайте список провайдеров, за исключением ChatBase
all_providers = [g4f.Provider.You,
                 g4f.Provider.Liaobots,
                 g4f.Provider.GptChatly]

# Подключение к базе данных SQLite
conn = sqlite3.connect(r'C:\Users\als19\Desktop\mysite\db.sqlite3')
cursor = conn.cursor()

# Получение списка статей, где content_review пустой или null, и content не начинается с "Error", "Reference #" и имеет длину более 100 символов
cursor.execute('SELECT id, content FROM news WHERE (content_review IS NULL OR content_review = "") AND NOT content LIKE "Error%" AND NOT content LIKE "Reference #%" AND LENGTH(content) > 100')
articles_to_process = cursor.fetchall()

# Флаг для отслеживания успешного выполнения хотя бы одной статьи
success_flag = False


import re

def filter_content(article_content):
    # Удаление ссылок вида [[1]](https://www.example.com)
    article_content = re.sub(r'\[\[\d+\]\]\([^)]+\)', '', article_content)

    # Удаление символов из вики [1]
    article_content = re.sub(r'\[\d+\]', '', article_content)

    # Удаление символов "####"
    article_content = re.sub(r'####', '', article_content)

    # Удаление строки "Title:"
    article_content = re.sub(r'Title:', '', article_content)

    # Удаление пробелов в начале и конце текста
    article_content = article_content.strip()

    return article_content



# Обход всех статей для обновления content_review
for article_id, original_content in articles_to_process:
    original_content = original_content[:5000]

    # Проверка условий для обновления content_review
    if original_content.startswith("Error") or original_content.startswith("Reference #") or len(original_content) < 100:
        content_review = "Error: Invalid content"
    else:
        current_provider_index = 0  # Индекс текущего провайдера

        while current_provider_index < len(all_providers):
            current_provider = all_providers[current_provider_index]

            try:
                # Использование GPT-3 для переписывания контента
                response = g4f.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"{original_content} write a similar article in the language of this article. Without words: title, end, abstract, and so on, only the text of the article itself."}],
                    provider=current_provider,
                )

                # Получение переписанного контента
                rewritten_content = filter_content(response)

                # Обновление столбца content_review в базе данных
                cursor.execute(
                    'UPDATE news SET content_review = ? WHERE id = ?', (rewritten_content, article_id))
                conn.commit()

                print(f"Контент успешно переписан и добавлен в столбец content_review для статьи с id {article_id} при использовании провайдера {current_provider.__name__}.")

                # Устанавливаем флаг успешного выполнения
                success_flag = True
                time.sleep(3)  # Задержка 5 секунд перед следующим запросом
                break  # Выход из цикла после успешного выполнения

            except Exception as e:
                print(f"При обработке статьи с id {article_id} провайдером {
                      current_provider.__name__} возникла ошибка:", e)
                current_provider_index += 1

                if current_provider_index >= len(all_providers):
                    print(
                        "Исчерпаны все провайдеры. Записываем ошибку и переходим к следующей статье.")
                    content_review = f"Error: {str(e)}"
                    cursor.execute(
                        'UPDATE news SET content_review = ? WHERE id = ?', (content_review, article_id))
                    conn.commit()

# Закрытие соединения с базой данных
conn.close()

# Если ни одна статья не обработана успешно
if not success_flag:
    print("Ни одна статья не смогла успешно выполнить задачу.")
