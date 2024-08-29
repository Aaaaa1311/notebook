# Пример теста при помощи cURL для добавления и получения заметки:

# Добавшление заметки 
bash
curl -u user1:password1 -X POST -H "Content-Type: application/json" -d '{"note": "Это тестовая заметка."}'


# Получение заметки
bash
curl -u user1:password1 http://127.0.0.1:5000/notes