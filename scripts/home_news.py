from django.shortcuts import render
import sqlite3

def index(request):
    # Получение самой новой новости с большими просмотрами от каждой страны
    latest_news_per_country = get_latest_news_per_country()

    context = {
        'latest_news_per_country': latest_news_per_country,
    }

    return render(request, 'index.html', context)


def get_latest_news_per_country():
    try:
        conn = sqlite3.connect(r'C:\Users\als19\Desktop\mysite\db.sqlite3')
        cursor = conn.cursor()

        # Добавлен отладочный вывод
        print("Before query execution")

        query = '''
            SELECT *
            FROM news
            WHERE (country_name, date, searches) IN (
                SELECT country_name, MAX(date) AS max_date, MAX(searches) AS max_searches
                FROM news
                GROUP BY country_name
            )
            ORDER BY date DESC, searches DESC
        '''

        cursor.execute(query)
        result = cursor.fetchall()

        # Добавлен отладочный вывод
        print("After query execution")

        print(result)  # Вывод для отладки
        return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


# Блок main для отладочных целей
if __name__ == "__main__":
    index(None)  # Вызов функции index для тестирования
