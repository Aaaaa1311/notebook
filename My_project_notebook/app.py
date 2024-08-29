from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import json
import os
import requests

# Инициализируем приложение Flask и объект аутентификации
app = Flask(__name__) 
auth = HTTPBasicAuth()

# Предустановленные пользователи. Создаем простой словарь для хранения пользователей и их паролей.
users = {
    "user1": "password1",
    "user2": "password2"
}

# Файл для хранения заметок
notes_storage = "notes.json"


# Создаем функции для работы с заметками в JSON-файле.

# 1. Функция для загрузки заметок из файла
def load_notes():
    if os.path.exists(notes_storage):
        with open(notes_storage, 'r') as f:
            return json.load(f)
    return {}

# 2. Функция для сохранения заметок в файл
def save_notes(notes):
    with open(notes_storage, 'w') as f:
        json.dump(notes, f)

# Функция для проверки пароля пользователя.
@auth.get_password
def get_pw(username):
    if username in users:
        return users[username]
    return None

# Функция для проверки текста на наличие орфографических ошибок с использованием API Яндекс.Спеллер.
def validate_spelling(text):
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    response = requests.post(url, data={'text': text})
    return response.json()

# Маршрут 'POST / notes' для добавления заметки
@app.route('/notes', methods=['POST'])
@auth.login_required
def add_note():
    data = request.json

    if 'note' not in data:
        return jsonify({'error': 'Ошибка'}), 400

    # Проверка орфографии
    spelling_errors = validate_spelling(data['note'])
    if spelling_errors:
        return jsonify({'error': 'Обнаружены орфографические ошибки', 'details': spelling_errors}), 400

    notes = load_notes()
    user_notes = notes.get(auth.current_user(), [])
    user_notes.append(data['note'])
    notes[auth.current_user()] = user_notes
    save_notes(notes)

    return jsonify({'message': 'Заметка добавлена'}), 201

# Маршрут 'GET / notes' для получения списка заметок
@app.route('/notes', methods=['GET'])
@auth.login_required
def get_notes():
    notes = load_notes()
    return jsonify(notes.get(auth.current_user(), []))



if __name__ == '__main__':
    app.run(debug=True)