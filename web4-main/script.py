import sqlite3
import hashlib

# Подключение к базе данных
conn = sqlite3.connect('./instance/site.db')
cursor = conn.cursor()

# SQL-запрос для вставки пользователей
sql_query = "INSERT INTO user_account (username, hashed_password, first_name, middle_name, role_id) VALUES (?, ?, ?, ?, ?)"

# Хэширование паролей с использованием hashlib
passwords = {
    'admin': 'password123',
    'user1': 'password456',
    'user2': 'password789'
}

for login, password in passwords.items():
    hashed_password = hashlib.md5(password.encode()).hexdigest()  # Хэширование пароля с использованием MD5
    user_data = (login, hashed_password, login, None, 1)  # Ваши данные пользователя
    try:
        cursor.execute(sql_query, user_data)
        conn.commit()  # Подтверждение транзакции после успешной вставки
    except sqlite3.IntegrityError:
        print(f"Пользователь '{login}' уже существует.")
        conn.rollback()  # Откат изменений, если произошла ошибка

# Закрытие соединения с базой данных
conn.close()
