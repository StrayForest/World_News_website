import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла
load_dotenv("api.env")  # Убедитесь, что это правильное имя файла

# Получение ключей API из переменных окружения
openai_api_key = os.getenv('OPENAI_API_KEY')

# Проверьте, что ключ API был успешно извлечен
if openai_api_key is None:
    raise ValueError("Не удалось получить OPENAI_API_KEY из переменных окружения")

# Создание клиента OpenAI
client = OpenAI(api_key=openai_api_key)

def generate_article(title, description):
    prompt = f"Напиши статью на основе этого заголовка: {title} и описания: {description}."
    response = client.completions.create(
        model="text-davinci-003",  # или другая модель, если доступно
        prompt=prompt,
        max_tokens=500
    )

    return response.choices[0].text

def main(title, description):

    article = generate_article(title, description)  # Сначала на английском

    return article

# Пример использования
title = "Проводница выбросила кота"
description = "Проводница выбросила из поезда кота, сбежавшего от пассажира"
generated_article = main(title, description)
print(generated_article)
