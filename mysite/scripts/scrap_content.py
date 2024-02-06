import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect(
    r'C:\Users\als19\Desktop\Google Trands Project\finnish_sites.db')
c = conn.cursor()

# Удаление дубликатов по столбцу url
c.execute('''
    DELETE FROM finnish_sites
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM finnish_sites
        GROUP BY url
    )
''')

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
conn.close()

print("Дубликаты по столбцу 'url' успешно удалены.")
