import sqlite3
import csv

# Подключение к базам данных
conn1 = sqlite3.connect('database1.db')
conn2 = sqlite3.connect('database2.db')

# Получение логина пользователя
user_login = input("Введите логин пользователя: ")

# Запрос для получения статистики по пользователю из базы данных 1
cursor1 = conn1.cursor()
cursor1.execute("SELECT post.header, author.login, COUNT(*) FROM post JOIN author ON post.author_id = author.id WHERE author.login = ? GROUP BY post.header, author.login", (user_login,))
data1 = cursor1.fetchall()

# Запрос для получения статистики по пользователю из базы данных 2
cursor2 = conn2.cursor()
cursor2.execute("SELECT datetime, COUNT(CASE WHEN event_type.type = 'login' THEN 1 END) AS logins, COUNT(CASE WHEN event_type.type = 'logout' THEN 1 END) AS logouts, COUNT(CASE WHEN event_type.type IN ('create_post', 'delete_post') THEN 1 END) AS blog_actions FROM logs JOIN event_type ON logs.event_type_id = event_type.id JOIN space_type ON logs.space_type_id = space_type.id WHERE user_id = ? GROUP BY datetime", (user_login,))
data2 = cursor2.fetchall()

# Запись результатов в CSV файлы
with open('comments.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["User Login", "Post Header", "Author Login", "Comment Count"])
    for row in data1:
        writer.writerow([user_login, row[0], row[1], row[2]])

with open('general.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Logins", "Logouts", "Blog Actions"])
    for row in data2:
        writer.writerow(row)

# Закрытие соединений с базами данных
conn1.close()
conn2.close()