import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJzdHJpbmciLCJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJwaG9uZSI6ODc3NTcxMTE4NDUsImV4cCI6MzkwMzU4NDY0Mjl9.R-wXsG08bq8WU-9tA-zYozLh-r-r8M179uKYKf5xEFE"

# Заголовок запроса с токеном JWT
headers = {
    "Authorization": f"Bearer {token}"
}


# URL защищенного эндпоинта
url = "http://127.0.0.1:8000/api/v1/test/protected"

# Отправка запроса POST к защищенному эндпоинту с использованием токена JWT и отправкой JSON данных
response = requests.get(url, headers=headers)

# Обработка ответа
if response.status_code == 200:
    print("Запрос успешно выполнен!")
    print("Ответ сервера:", response.json())
else:
    print("Ошибка при выполнении запроса:", response.status_code)
